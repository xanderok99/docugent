import React from 'react';
import styles from './Sidebar.module.css';
import { FiMessageSquare, FiClock, FiSettings, FiPlus } from 'react-icons/fi';

const Sidebar: React.FC = () => {
  return (
    <aside className={styles.sidebar}>
      <div className={styles.logo}>
        <img src="https://apiconf.net/logo2025.svg" alt="APIConf Logo" />
      </div>

      <button className={styles.newChatButton}>
        <FiPlus />
        New Chat
      </button>

      <nav className={styles.nav}>
        <a href="#" className={styles.active}>
          <FiMessageSquare />
          Chats
        </a>
        <a href="#">
          <FiClock />
          History
        </a>
        <a href="#">
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
  );
};

export default Sidebar; 