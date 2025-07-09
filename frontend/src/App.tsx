import Chat from './components/Chat';
import Sidebar from './components/Sidebar';
import styles from './App.module.css';
import { useState, useEffect } from 'react';

const saveSessionToHistory = () => {
  const history = JSON.parse(localStorage.getItem('apiconf_chat_history') || '[]');
  const sessionId = localStorage.getItem('apiconf_session_id');
  const timestamp = new Date().toLocaleString();
  history.unshift({ sessionId, timestamp });
  localStorage.setItem('apiconf_chat_history', JSON.stringify(history.slice(0, 10)));
};

const HistoryComponent = ({ resetSignal, view }: { resetSignal: number, view: string }) => {
  const [history, setHistory] = useState<{ sessionId: string, timestamp: string }[]>([]);
  useEffect(() => {
    setHistory(JSON.parse(localStorage.getItem('apiconf_chat_history') || '[]'));
  }, [resetSignal, view]);
  return (
    <div style={{ padding: 24 }}>
      <h2>Recent Chats</h2>
      {history.length === 0 ? <div>No recent chats.</div> : (
        <ul>
          {history.map((item, idx) => (
            <li key={item.sessionId + idx}>
              <span>{item.timestamp}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
const SettingsComponent = () => <div>Settings view coming soon.</div>;

const App: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [view, setView] = useState<'chat' | 'history' | 'settings'>('chat');
  const [resetSignal, setResetSignal] = useState(0);

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <div className={styles.app}>
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onNewChat={() => { setView('chat'); setSidebarOpen(false); setResetSignal(s => s + 1); saveSessionToHistory(); }}
        onShowHistory={() => { setView('history'); setSidebarOpen(false); }}
        onShowSettings={() => { setView('settings'); setSidebarOpen(false); }}
        activeView={view}
      />
      <main>
        {view === 'chat' && <Chat onMenuClick={toggleSidebar} resetSignal={resetSignal} />}
        {view === 'history' && <HistoryComponent resetSignal={resetSignal} view={view} />}
        {view === 'settings' && <SettingsComponent />}
      </main>
    </div>
  );
};

export default App;
