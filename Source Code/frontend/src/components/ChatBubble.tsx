import React from 'react';
import { motion } from 'framer-motion';
import { MarkdownRenderer } from './MarkdownRenderer';
import type { ChatMessage } from '../stores/useChatStore';

const TypingIndicator = () => (
  <div className="flex items-center gap-1 px-1 py-2">
    {[0, 1, 2].map((i) => (
      <motion.span
        key={i}
        animate={{ y: [0, -5, 0], opacity: [0.3, 1, 0.3] }}
        transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.15 }}
        className="w-1.5 h-1.5 rounded-full bg-primary"
      />
    ))}
  </div>
);

interface ChatBubbleProps {
  message: ChatMessage;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  if (isUser) {
    return (
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="flex justify-end">
        <div className="max-w-[80%]">
          <div className="glass-panel p-4 bg-surface-active/40 border-primary/20 shadow-lg">
            <p className="text-text-main text-[15px] leading-relaxed whitespace-pre-wrap">
              {message.content}
            </p>
          </div>
        </div>
      </motion.div>
    );
  }

  // Assistant message
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="flex justify-start">
      <div className="max-w-[85%] min-w-[200px]">
        <div className="flex items-center gap-3 mb-2 px-1">
          <div className={`w-6 h-6 rounded-md flex items-center justify-center shadow-lg border 
            ${message.isStreaming 
              ? 'bg-gradient-to-br from-primary to-purple-600 shadow-[0_0_15px_rgba(59,130,246,0.4)] border-primary/50 animate-pulse' 
              : 'bg-gradient-to-br from-primary to-purple-600 border-primary/30'}`}>
            <span className="text-[10px] font-bold text-white">L</span>
          </div>
          <span className="text-sm font-semibold text-text-main text-glow">LUFFY</span>
          {message.error && <span className="text-xs text-red-400 ml-2">Error</span>}
        </div>
        
        <div className={`glass-panel p-5 shadow-xl space-y-4 ${message.error ? 'bg-red-900/10 border-red-500/50' : 'bg-surface/30'}`}>
          {message.content ? (
            <div className="text-[15px] leading-relaxed text-text-main">
               <MarkdownRenderer content={message.content} />
            </div>
          ) : message.isStreaming && !message.content ? (
            <TypingIndicator />
          ) : null}
        </div>
      </div>
    </motion.div>
  );
};
