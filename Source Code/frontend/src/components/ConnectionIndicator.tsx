import React, { useEffect } from 'react';
import { Activity, Server, Database, AlertCircle } from 'lucide-react';
import { useChatStore } from '../stores/useChatStore';
import { ChatService } from '../services/ChatService';

export const ConnectionIndicator: React.FC = () => {
  const { connectionStatus, ollamaStatus, currentProvider, currentModel, isStreaming, error } = useChatStore();

  useEffect(() => {
    ChatService.checkHealth();
    const interval = setInterval(() => {
      ChatService.checkHealth();
    }, 10000); // Check every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected': return 'bg-green-500';
      case 'disconnected': return 'bg-red-500';
      case 'checking': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="flex flex-col space-y-1">
      <div className="flex items-center space-x-3 text-xs">
        {/* Backend Status */}
        <div className="flex items-center space-x-1.5 bg-gray-800/50 rounded-full px-2.5 py-1 border border-gray-700/50 transition-colors">
          <Server size={12} className={connectionStatus === 'connected' ? 'text-green-400' : 'text-gray-400'} />
          <span className="text-gray-300 hidden sm:inline">Backend</span>
          <div className={`w-2 h-2 rounded-full ${getStatusColor(connectionStatus)}`} />
        </div>
        
        {/* Provider Status */}
        <div className="flex items-center space-x-1.5 bg-gray-800/50 rounded-full px-2.5 py-1 border border-gray-700/50 transition-colors">
          <Database size={12} className={ollamaStatus === 'connected' ? 'text-green-400' : 'text-gray-400'} />
          <span className="text-gray-300 hidden sm:inline">{currentProvider}</span>
          <div className={`w-2 h-2 rounded-full ${getStatusColor(ollamaStatus)}`} />
        </div>

        {/* Model & Streaming */}
        <div className="flex items-center space-x-1.5 bg-gray-800/50 rounded-full px-2.5 py-1 border border-gray-700/50">
          <Activity size={12} className={isStreaming ? 'text-blue-400 animate-pulse' : 'text-gray-400'} />
          <span className="text-gray-300 font-mono">{currentModel}</span>
        </div>
      </div>
      
      {/* Error State */}
      {error && (
        <div className="flex items-center space-x-1.5 text-xs text-red-400 bg-red-900/20 px-2.5 py-1 rounded-md border border-red-900/50">
          <AlertCircle size={12} />
          <span className="truncate max-w-[250px]">{error}</span>
        </div>
      )}
    </div>
  );
};
