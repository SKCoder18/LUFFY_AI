import { HashRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { ChatPage } from './components/ChatPage';
import { MiniOverlay, FloatingOrb } from './components/SpecialWindows';
import { SettingsPage, MemoryPage, VisionPage, ToolsPage } from './pages/PlaceholderPages';

export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/mini" element={<MiniOverlay />} />
        <Route path="/orb" element={<FloatingOrb />} />
        
        {/* Dashboard Routes */}
        <Route path="/dashboard/*" element={
          <Layout>
            <Routes>
              <Route path="/" element={<ChatPage />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/memory" element={<MemoryPage />} />
              <Route path="/vision" element={<VisionPage />} />
              <Route path="/tools" element={<ToolsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </Layout>
        } />
        
        {/* Default route redirects to dashboard chat for now */}
        <Route path="*" element={
          <Layout>
            <ChatPage />
          </Layout>
        } />
      </Routes>
    </HashRouter>
  );
}
