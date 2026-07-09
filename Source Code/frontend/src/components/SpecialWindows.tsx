import { motion } from 'framer-motion';

export const MiniOverlay = () => {
  return (
    <div className="h-screen w-screen flex flex-col items-center justify-start pt-[20vh] bg-transparent text-text-main font-sans">
      <motion.div 
        initial={{ opacity: 0, y: -20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
        className="w-[600px] glass-panel bg-surface/80 shadow-[0_20px_50px_rgba(0,0,0,0.5)] border border-primary/20 rounded-2xl overflow-hidden drag-region"
      >
        <div className="flex items-center px-4 py-3 gap-3 no-drag-region">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center shadow-lg shadow-primary/20">
            <span className="font-bold text-white text-lg">L</span>
          </div>
          <input 
            type="text" 
            autoFocus 
            placeholder="Ask LUFFY anything..." 
            className="flex-1 bg-transparent border-none outline-none text-xl font-medium text-text-main placeholder-text-muted/50"
          />
          <div className="flex gap-1 text-[10px] font-bold text-text-muted/60 uppercase tracking-widest bg-surface px-2 py-1 rounded-md border border-border">
            <span>Esc</span>
          </div>
        </div>
        
        {/* Placeholder Results Area */}
        <div className="px-4 py-2 border-t border-border/50 bg-surface-active/30 text-xs text-text-muted flex justify-between">
          <span>Search, calculate, or ask...</span>
          <span className="flex items-center gap-1">Press <kbd className="font-mono bg-surface px-1 rounded border border-border">Enter</kbd></span>
        </div>
      </motion.div>
    </div>
  );
};

export const FloatingOrb = () => {
  return (
    <div className="h-screen w-screen flex items-center justify-center drag-region bg-transparent">
      <motion.div 
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="relative flex items-center justify-center cursor-pointer group"
      >
        {/* Outer glowing halo */}
        <motion.div 
          animate={{ rotate: 360 }}
          transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
          className="absolute inset-0 rounded-full bg-gradient-to-tr from-primary/30 via-purple-500/30 to-blue-400/30 blur-xl group-hover:blur-2xl transition-all duration-300"
        />
        
        {/* Inner rotating rings */}
        <motion.div 
          animate={{ rotate: -360, scale: [1, 1.05, 1] }}
          transition={{ rotate: { duration: 8, repeat: Infinity, ease: "linear" }, scale: { duration: 3, repeat: Infinity, ease: "easeInOut" } }}
          className="w-16 h-16 rounded-full border-2 border-dashed border-primary/40 absolute"
        />

        {/* The Core Orb */}
        <div className="w-14 h-14 rounded-full bg-gradient-to-br from-primary via-blue-600 to-purple-700 shadow-[0_0_20px_rgba(59,130,246,0.6)] flex items-center justify-center relative overflow-hidden">
          {/* Glass reflection */}
          <div className="absolute inset-0 bg-gradient-to-b from-white/20 to-transparent rounded-full pointer-events-none" />
          
          {/* Center core pulse */}
          <motion.div 
            animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            className="w-6 h-6 rounded-full bg-white blur-[2px]"
          />
        </div>
      </motion.div>
    </div>
  );
};
