import React from 'react';
import { motion } from 'framer-motion';
import { Settings, Database, Eye, Wrench } from 'lucide-react';

const PageWrapper = ({ children, title, icon: Icon }: { children: React.ReactNode, title: string, icon: any }) => (
  <motion.div 
    initial={{ opacity: 0, y: 10 }} 
    animate={{ opacity: 1, y: 0 }} 
    exit={{ opacity: 0, y: -10 }} 
    transition={{ duration: 0.2 }}
    className="h-full flex flex-col p-8"
  >
    <div className="flex items-center gap-3 mb-8">
      <div className="w-10 h-10 rounded-xl bg-surface-active border border-border flex items-center justify-center text-primary shadow-lg">
        <Icon size={20} />
      </div>
      <h1 className="text-2xl font-bold tracking-tight">{title}</h1>
    </div>
    <div className="flex-1 overflow-y-auto premium-scrollbar pr-4">
      {children}
    </div>
  </motion.div>
);

export const SettingsPage = () => (
  <PageWrapper title="Settings" icon={Settings}>
    <div className="space-y-6">
      <div className="glass-panel p-6 space-y-4">
        <h2 className="text-lg font-semibold text-text-main border-b border-border/50 pb-2">AI Provider</h2>
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium">Ollama Core</p>
            <p className="text-sm text-text-muted">Local execution (llama3.2:3b)</p>
          </div>
          <div className="w-12 h-6 rounded-full bg-primary relative cursor-pointer">
            <div className="absolute right-1 top-1 w-4 h-4 rounded-full bg-white shadow-sm" />
          </div>
        </div>
      </div>
      {/* Skeleton rows */}
      <div className="glass-panel p-6 space-y-4">
         <h2 className="text-lg font-semibold text-text-main border-b border-border/50 pb-2">Preferences</h2>
         {[1, 2, 3].map(i => (
           <div key={i} className="flex items-center justify-between py-2">
             <div className="w-48 h-4 bg-surface-active rounded-md animate-pulse" />
             <div className="w-8 h-4 bg-surface-active rounded-md animate-pulse" />
           </div>
         ))}
      </div>
    </div>
  </PageWrapper>
);

export const MemoryPage = () => (
  <PageWrapper title="Long-Term Memory" icon={Database}>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {[1, 2, 3, 4].map(i => (
        <div key={i} className="glass-panel p-5 hover:bg-surface-hover transition-colors cursor-pointer group">
          <div className="flex justify-between items-start mb-3">
            <div className="w-32 h-4 bg-surface-active rounded group-hover:bg-primary/20 transition-colors" />
            <span className="text-xs text-text-muted">2 hours ago</span>
          </div>
          <div className="space-y-2">
            <div className="w-full h-3 bg-surface rounded" />
            <div className="w-5/6 h-3 bg-surface rounded" />
            <div className="w-4/6 h-3 bg-surface rounded" />
          </div>
        </div>
      ))}
    </div>
  </PageWrapper>
);

export const VisionPage = () => (
  <PageWrapper title="Vision & Screen" icon={Eye}>
    <div className="flex flex-col items-center justify-center h-full text-center space-y-4 opacity-60">
      <div className="w-24 h-24 rounded-2xl bg-surface-active border border-border flex items-center justify-center text-text-muted mb-4">
        <Eye size={40} />
      </div>
      <h3 className="text-xl font-medium">Screen Context Disabled</h3>
      <p className="text-text-muted max-w-md">
        LUFFY cannot currently see your screen. Enable screen capture permissions in Settings to allow contextual understanding.
      </p>
      <button className="glass-button mt-4">
        Request Permissions
      </button>
    </div>
  </PageWrapper>
);

export const ToolsPage = () => (
  <PageWrapper title="Automation Tools" icon={Wrench}>
    <div className="space-y-4">
      {['File Explorer', 'Terminal', 'VS Code', 'Browser', 'System Settings'].map((tool, idx) => (
        <div key={idx} className="glass-panel p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-lg bg-surface flex items-center justify-center text-primary/70">
              <Wrench size={18} />
            </div>
            <div>
              <p className="font-medium">{tool}</p>
              <p className="text-xs text-text-muted">Local automation module</p>
            </div>
          </div>
          <button className="px-3 py-1.5 rounded-md bg-surface-active text-xs font-medium border border-border hover:border-primary/50 transition-colors">
            Configure
          </button>
        </div>
      ))}
    </div>
  </PageWrapper>
);
