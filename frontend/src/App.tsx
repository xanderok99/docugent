import React from 'react';
import styles from './App.module.css';
import Chat from './components/Chat';
import Sidebar from './components/Sidebar';

const App: React.FC = () => {
  return (
    <div className={styles.app}>
      <Sidebar />
      <main>
        <Chat />
      </main>
    </div>
  );
};

export default App; 