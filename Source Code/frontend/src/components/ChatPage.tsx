import React, { useRef, useEffect, useState } from 'react';
import { Send, Image as ImageIcon, Paperclip, StopCircle, RefreshCw } from 'lucide-react';
import { ChatBubble } from './ChatBubble';
import { useChatStore } from '../stores/useChatStore';
import { ChatService } from '../services/ChatService';

export const ChatPage = () => {
  const { messages, isStreaming, cancelGeneration } = useChatStore();
  const [input, setInput] = useState('');
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [isAutoScrollEnabled, setIsAutoScrollEnabled] = useState(true);

  // Scroll to bottom logic
  const scrollToBottom = () => {
    if (isAutoScrollEnabled) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isStreaming]);

  // Handle scroll lock if user scrolls up
  const handleScroll = () => {
    if (!scrollContainerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = scrollContainerRef.current;
    
    // If we are within 50px of the bottom, enable auto-scroll
    const isNearBottom = scrollHeight - scrollTop - clientHeight < 50;
    setIsAutoScrollEnabled(isNearBottom);
  };

  const handleSend = () => {
    if (!input.trim() || isStreaming) return;
    ChatService.sendMessage(input.trim());
    setInput('');
    setIsAutoScrollEnabled(true);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-transparent">
      {/* Messages Area */}
      <div 
        ref={scrollContainerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto p-6 space-y-6 premium-scrollbar"
      >
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full opacity-50 space-y-4">
             <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center shadow-2xl border border-primary/30">
                <span className="text-3xl font-bold text-white">L</span>
             </div>
             <p className="text-text-muted">How can I help you today?</p>
          </div>
        ) : (
          messages.map((msg) => (
            <ChatBubble key={msg.id} message={msg} />
          ))
        )}
        <div ref={messagesEndRef} className="h-4" /> {/* Bottom Padding */}
      </div>

      {/* Input Area */}
      <div className="p-6 pt-2 bg-gradient-to-t from-background via-background to-transparent z-10 relative">
        {isStreaming && (
          <div className="absolute -top-10 left-1/2 transform -translate-x-1/2">
             <button 
               onClick={() => cancelGeneration()}
               className="flex items-center gap-2 bg-red-500/20 hover:bg-red-500/40 border border-red-500/50 text-red-200 px-4 py-1.5 rounded-full shadow-lg transition-all text-sm backdrop-blur-md"
             >
                <StopCircle size={16} /> Stop Generation
             </button>
          </div>
        )}
        
        {!isStreaming && messages.length > 0 && messages[messages.length - 1].role === 'assistant' && (
           <div className="absolute -top-10 left-1/2 transform -translate-x-1/2">
             <button 
               onClick={() => ChatService.regenerateLastResponse()}
               className="flex items-center gap-2 bg-surface hover:bg-surface-active border border-border text-text-muted hover:text-text-main px-4 py-1.5 rounded-full shadow-lg transition-all text-sm backdrop-blur-md"
             >
                <RefreshCw size={14} /> Regenerate
             </button>
           </div>
        )}

        <div className="glass-panel p-2 flex flex-col gap-2 border-primary/20 shadow-[0_0_30px_rgba(0,0,0,0.5)] focus-within:border-primary/50 focus-within:shadow-[0_0_20px_rgba(59,130,246,0.15)] transition-all duration-300">
          <textarea 
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Message LUFFY... (Shift+Enter for new line)" 
            className="w-full bg-transparent border-none outline-none text-[15px] resize-none px-3 py-2 text-text-main placeholder-text-muted hide-scrollbar"
            style={{ minHeight: '40px', maxHeight: '200px' }}
          />
          <div className="flex items-center justify-between px-2 pb-1">
            <div className="flex items-center gap-1">
              <button className="p-1.5 rounded-lg text-text-muted hover:text-text-main hover:bg-surface transition-colors disabled:opacity-50" disabled={isStreaming}><Paperclip size={18} /></button>
              <button className="p-1.5 rounded-lg text-text-muted hover:text-text-main hover:bg-surface transition-colors disabled:opacity-50" disabled={isStreaming}><ImageIcon size={18} /></button>
            </div>
            <button 
              onClick={handleSend}
              disabled={!input.trim() || isStreaming}
              className="p-1.5 px-3 rounded-lg bg-primary hover:bg-primary-hover text-white flex items-center gap-2 shadow-[0_0_15px_rgba(59,130,246,0.4)] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span className="text-sm font-semibold">Send</span>
              <Send size={16} />
            </button>
          </div>
        </div>
        <div className="text-center mt-3 text-[11px] text-text-muted/60">
          LUFFY AI runs locally. Your data remains on your machine.
        </div>
      </div>
    </div>
  );
};
