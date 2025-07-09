import { Route, Routes } from 'react-router-dom';

import Chat from './components/Chat';
import Sidebar from './components/Sidebar';
import styles from './App.module.css';
import { useState } from 'react';

const App: React.FC = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => setSidebarOpen(!isSidebarOpen);
  const closeSidebar = () => setSidebarOpen(false);

  return (
    <div className={styles.app}>
      <Sidebar isOpen={isSidebarOpen} onClose={closeSidebar} />
      <main>
        <Routes>
          <Route path="/" element={<Chat onMenuClick={toggleSidebar} />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
