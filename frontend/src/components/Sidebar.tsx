import React, { useEffect } from 'react';
import styles from './Sidebar.module.css';
import { FiMessageSquare, FiClock, FiSettings, FiPlus, FiX } from 'react-icons/fi';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  onNewChat: () => void;
  onShowHistory: () => void;
  onShowSettings: () => void;
  activeView: 'chat' | 'history' | 'settings';
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose, onNewChat, onShowHistory, onShowSettings, activeView }) => {
  useEffect(() => {
    if (isOpen && window.innerWidth <= 768) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  return (
    <>
      {isOpen && <div className={styles.overlay} onClick={onClose}></div>}
      <aside
        className={`${styles.sidebar} ${isOpen ? styles.open : ''}`}
        role="dialog"
        aria-modal="true"
        aria-label="Sidebar navigation"
      >
        <div className={styles.logo}>
          <img src="https://apiconf.net/logo2025.svg" alt="APIConf Logo" />
          <button className={styles.closeButton} onClick={onClose}>
            <FiX />
          </button>
        </div>

        <button className={styles.newChatButton} onClick={onNewChat}>
          <FiPlus />
          New Chat
        </button>

        <nav className={styles.nav}>
          <a href="#" className={activeView === 'chat' ? styles.active : ''} onClick={e => { e.preventDefault(); onNewChat(); }}>
            <FiMessageSquare />
            Chats
          </a>
          <a href="#" className={activeView === 'history' ? styles.active : ''} onClick={e => { e.preventDefault(); onShowHistory(); }}>
            <FiClock />
            History
          </a>
          <a href="#" className={activeView === 'settings' ? styles.active : ''} onClick={e => { e.preventDefault(); onShowSettings(); }}>
            <FiSettings />
            Settings
          </a>
        </nav>

        <div className={styles.recentChats}>
          <h3>Recent Chats</h3>
          <div className={styles.chatItem}>What is the schedule?</div>
          <div className={styles.chatItem}>Who is speaking about APIs?</div>
          <div className={styles.chatItem}>Directions to the venue</div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar; 