import React, { useState } from 'react';
import styles from './App.module.css';
import Chat from './components/Chat';
import Sidebar from './components/Sidebar';

const App: React.FC = () => {
  const [isSidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!isSidebarOpen);
  };
  
  const closeSidebar = () => {
    setSidebarOpen(false);
  }

  return (
    <div className={styles.app}>
      <Sidebar isOpen={isSidebarOpen} onClose={closeSidebar} />
      <main>
        <Chat onMenuClick={toggleSidebar} />
      </main>
    </div>
  );
};

export default App; 