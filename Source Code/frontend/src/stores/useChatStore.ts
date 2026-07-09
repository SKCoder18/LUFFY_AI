import { create } from 'zustand';

export type MessageRole = 'user' | 'assistant' | 'system';

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  isStreaming?: boolean;
  error?: boolean;
}

export interface ChatState {
  messages: ChatMessage[];
  isStreaming: boolean;
  connectionStatus: 'connected' | 'disconnected' | 'checking';
  ollamaStatus: 'connected' | 'disconnected' | 'checking';
  currentProvider: string;
  currentModel: string;
  error: string | null;
  abortController: AbortController | null;

  // Actions
  addMessage: (message: Omit<ChatMessage, 'id'>) => string;
  updateMessage: (id: string, content: string, isStreaming?: boolean, error?: boolean) => void;
  appendMessageContent: (id: string, chunk: string) => void;
  setStreaming: (status: boolean) => void;
  setConnectionStatus: (status: 'connected' | 'disconnected' | 'checking') => void;
  setOllamaStatus: (status: 'connected' | 'disconnected' | 'checking') => void;
  setProviderInfo: (provider: string, model: string) => void;
  setError: (error: string | null) => void;
  setAbortController: (controller: AbortController | null) => void;
  cancelGeneration: () => void;
  clearMessages: () => void;
  removeLastMessage: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isStreaming: false,
  connectionStatus: 'checking',
  ollamaStatus: 'checking',
  currentProvider: 'Ollama',
  currentModel: 'llama3.2:3b',
  error: null,
  abortController: null,

  addMessage: (message) => {
    const id = Date.now().toString() + Math.random().toString(36).substring(7);
    set((state) => ({
      messages: [...state.messages, { ...message, id }],
    }));
    return id;
  },

  updateMessage: (id, content, isStreaming = false, error = false) => {
    set((state) => ({
      messages: state.messages.map((msg) =>
        msg.id === id ? { ...msg, content, isStreaming, error } : msg
      ),
    }));
  },

  appendMessageContent: (id, chunk) => {
    set((state) => ({
      messages: state.messages.map((msg) =>
        msg.id === id ? { ...msg, content: msg.content + chunk } : msg
      ),
    }));
  },

  setStreaming: (status) => set({ isStreaming: status }),
  setConnectionStatus: (status) => set({ connectionStatus: status }),
  setOllamaStatus: (status) => set({ ollamaStatus: status }),
  setProviderInfo: (provider, model) => set({ currentProvider: provider, currentModel: model }),
  setError: (error) => set({ error }),
  setAbortController: (controller) => set({ abortController: controller }),

  cancelGeneration: () => {
    const { abortController } = get();
    if (abortController) {
      abortController.abort();
      set({ abortController: null, isStreaming: false });
    }
  },

  clearMessages: () => set({ messages: [] }),
  
  removeLastMessage: () => set((state) => {
    if (state.messages.length === 0) return state;
    return { messages: state.messages.slice(0, -1) };
  })
}));
