import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MessageSquare, Database, Eye, Wrench, Settings, Search, Bell } from 'lucide-react';
import { ConnectionIndicator } from './ConnectionIndicator';

const Sidebar = () => {
  const location = useLocation();
  const navItems = [
    { path: '/dashboard/chat', icon: MessageSquare, label: 'Chat' },
    { path: '/dashboard/memory', icon: Database, label: 'Memory' },
    { path: '/dashboard/vision', icon: Eye, label: 'Vision' },
    { path: '/dashboard/tools', icon: Wrench, label: 'Tools' },
  ];

  return (
    <div className="w-[72px] flex flex-col items-center py-6 bg-black/40 backdrop-blur-3xl border-r border-border z-10 drag-region shadow-2xl">
      <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary/20 to-purple-600/20 flex items-center justify-center mb-8 border border-primary/30 shadow-[0_0_20px_rgba(59,130,246,0.15)] no-drag-region cursor-pointer group">
        <span className="font-bold text-primary text-xl text-glow group-hover:scale-110 transition-transform">L</span>
      </div>
      
      <div className="flex-1 flex flex-col gap-4 no-drag-region w-full px-3">
        {navItems.map((item) => {
          const isActive = location.pathname.startsWith(item.path) || (item.path === '/dashboard/chat' && location.pathname === '/dashboard');
          return (
            <Link key={item.path} to={item.path} className="relative flex justify-center py-3 rounded-xl group transition-all duration-300">
              {isActive && (
                <motion.div layoutId="sidebar-active" className="absolute inset-0 bg-primary/10 border border-primary/20 rounded-xl" transition={{ type: "spring", stiffness: 300, damping: 30 }} />
              )}
              <item.icon size={22} className={`relative z-10 transition-colors duration-300 ${isActive ? 'text-primary' : 'text-text-muted group-hover:text-text-main'}`} />
            </Link>
          );
        })}
      </div>

      <div className="no-drag-region w-full px-3 mb-2">
        <Link to="/dashboard/settings" className="relative flex justify-center py-3 rounded-xl group transition-all duration-300">
          {location.pathname.startsWith('/dashboard/settings') && (
             <motion.div layoutId="sidebar-active" className="absolute inset-0 bg-primary/10 border border-primary/20 rounded-xl" transition={{ type: "spring", stiffness: 300, damping: 30 }} />
          )}
          <Settings size={22} className={`relative z-10 transition-colors duration-300 ${location.pathname.startsWith('/dashboard/settings') ? 'text-primary' : 'text-text-muted group-hover:text-text-main'}`} />
        </Link>
      </div>
    </div>
  );
};

const Header = () => (
  <header className="h-14 border-b border-border flex items-center justify-between px-6 drag-region bg-black/20 backdrop-blur-md">
    <div className="flex items-center gap-2">
      <span className="text-sm font-semibold tracking-wider text-text-muted">LUFFY AI</span>
      <span className="px-2 py-0.5 rounded-full bg-surface-active text-[10px] uppercase font-bold tracking-widest border border-border">Local</span>
    </div>
    <div className="flex items-center gap-4 no-drag-region">
      <button className="text-text-muted hover:text-text-main transition-colors"><Search size={18} /></button>
      <button className="text-text-muted hover:text-text-main transition-colors relative">
        <Bell size={18} />
        <span className="absolute 0 top-0 right-0 w-2 h-2 bg-primary rounded-full animate-pulse border border-background"></span>
      </button>
    </div>
  </header>
);

const StatusBar = () => (
  <footer className="h-8 border-t border-border flex items-center justify-between px-4 text-xs text-text-muted bg-black/40 backdrop-blur-md z-10">
    <div className="flex items-center gap-3">
      <ConnectionIndicator />
      <div className="w-px h-3 bg-border"></div>
      <div>RAM: 142MB</div>
    </div>
    <div>v2.0.0-beta</div>
  </footer>
);

export const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="flex h-screen w-screen bg-transparent overflow-hidden text-text-main font-sans">
      <Sidebar />
      <div className="flex-1 flex flex-col relative z-0 bg-background/90 shadow-2xl overflow-hidden">
        <Header />
        <main className="flex-1 overflow-hidden relative">
          {children}
        </main>
        <StatusBar />
      </div>
    </div>
  );
};
