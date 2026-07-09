import { useChatStore } from '../stores/useChatStore';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

export class ChatService {
  static async checkHealth() {
    const store = useChatStore.getState();
    store.setConnectionStatus('checking');
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.ok) {
        const data = await response.json();
        store.setConnectionStatus('connected');
        if (data.provider === 'connected') {
          store.setOllamaStatus('connected');
        } else {
          store.setOllamaStatus('disconnected');
        }
      } else {
        store.setConnectionStatus('disconnected');
        store.setOllamaStatus('disconnected');
      }
    } catch (error) {
      store.setConnectionStatus('disconnected');
      store.setOllamaStatus('disconnected');
    }
  }

  static async sendMessage(content: string) {
    const store = useChatStore.getState();
    
    // Add user message
    store.addMessage({ role: 'user', content });
    
    // Add empty assistant message placeholder
    const assistantMsgId = store.addMessage({ role: 'assistant', content: '', isStreaming: true });
    
    store.setStreaming(true);
    store.setError(null);
    
    const abortController = new AbortController();
    store.setAbortController(abortController);

    // Prepare payload
    // Only send non-error messages as context
    const contextMessages = useChatStore.getState().messages
      .filter(m => !m.error && m.id !== assistantMsgId)
      .map(m => ({ role: m.role, content: m.content }));

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: contextMessages,
          model: store.currentModel
        }),
        signal: abortController.signal,
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      if (!response.body) {
        throw new Error('ReadableStream not supported by the browser.');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      
      let done = false;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          store.appendMessageContent(assistantMsgId, chunk);
        }
      }

      store.updateMessage(assistantMsgId, useChatStore.getState().messages.find(m => m.id === assistantMsgId)?.content || '', false, false);
      
    } catch (error: any) {
      if (error.name === 'AbortError') {
        store.updateMessage(assistantMsgId, useChatStore.getState().messages.find(m => m.id === assistantMsgId)?.content + ' [Cancelled]', false, false);
      } else {
        console.error('Chat stream error:', error);
        store.updateMessage(assistantMsgId, useChatStore.getState().messages.find(m => m.id === assistantMsgId)?.content || '', false, true);
        store.setError(error.message || 'Failed to connect to backend.');
      }
    } finally {
      store.setStreaming(false);
      store.setAbortController(null);
    }
  }

  static regenerateLastResponse() {
    const store = useChatStore.getState();
    const messages = store.messages;
    
    if (messages.length < 2) return;
    
    const lastMsg = messages[messages.length - 1];
    if (lastMsg.role === 'assistant') {
      // Find the last user message
      const lastUserMsg = messages.slice().reverse().find(m => m.role === 'user');
      if (lastUserMsg) {
        // Remove the assistant message
        store.removeLastMessage();
        // Resend the last user message text via context
        // Wait, to regenerate we just pop the last assistant message and trigger sendMessage without adding a new user message.
        // Actually, sendMessage adds a user message. Let's make a dedicated method.
        this._resendWithoutAddingUser();
      }
    }
  }
  
  static async _resendWithoutAddingUser() {
    const store = useChatStore.getState();
    const assistantMsgId = store.addMessage({ role: 'assistant', content: '', isStreaming: true });
    store.setStreaming(true);
    store.setError(null);
    const abortController = new AbortController();
    store.setAbortController(abortController);

    const contextMessages = useChatStore.getState().messages
      .filter(m => !m.error && m.id !== assistantMsgId)
      .map(m => ({ role: m.role, content: m.content }));

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: contextMessages, model: store.currentModel }),
        signal: abortController.signal,
      });

      if (!response.ok) throw new Error(`Server error ${response.status}`);
      if (!response.body) throw new Error('ReadableStream not supported');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      
      let done = false;
      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          store.appendMessageContent(assistantMsgId, chunk);
        }
      }
      store.updateMessage(assistantMsgId, useChatStore.getState().messages.find(m => m.id === assistantMsgId)?.content || '', false, false);
    } catch (error: any) {
      if (error.name === 'AbortError') {
        store.updateMessage(assistantMsgId, useChatStore.getState().messages.find(m => m.id === assistantMsgId)?.content + ' [Cancelled]', false, false);
      } else {
        store.updateMessage(assistantMsgId, useChatStore.getState().messages.find(m => m.id === assistantMsgId)?.content || '', false, true);
        store.setError(error.message);
      }
    } finally {
      store.setStreaming(false);
      store.setAbortController(null);
    }
  }
}
