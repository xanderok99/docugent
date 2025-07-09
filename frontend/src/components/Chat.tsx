import { FiMenu, FiSend } from 'react-icons/fi';
import React, { useCallback, useEffect, useRef, useState } from 'react';

import ReactMarkdown from 'react-markdown';
import TypingIndicator from './TypingIndicator';
import remarkGfm from 'remark-gfm';
import styles from './Chat.module.css';
import { useSearchParams } from 'react-router-dom';

interface Message {
  text: string;
  sender: 'user' | 'bot';
  timestamp: string;
}

interface ChatProps {
  onMenuClick: () => void;
}

const Chat: React.FC<ChatProps> = ({ onMenuClick }) => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [processedMessages, setProcessedMessages] = useState<Set<string>>(new Set());
  const [hasProcessedUrlMessage, setHasProcessedUrlMessage] = useState(false);

  const handleSend = useCallback(async (messageToSend: string) => {
    if (!messageToSend.trim()) return;

    if (processedMessages.has(messageToSend)) {
      console.log('Message already processed:', messageToSend);
      return;
    }

    console.log('Sending message to /api/v1/agents/chat:', messageToSend);

    const userMessage: Message = {
      text: messageToSend,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setIsTyping(true);

    try {
      const response = await fetch('/api/v1/agents/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageToSend,
          user_id: '12345',
          session_id: 'abcde',
        }),
      });

      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status}`);
      }

      const result = await response.json();
      console.log('API response:', result);

      const botMessage: Message = {
        text: result.data.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prevMessages) => [...prevMessages, botMessage]);
      setProcessedMessages((prev) => new Set(prev).add(messageToSend));

      // Clear URL parameters after processing
      if (window.location.search) {
        window.history.replaceState({}, document.title, window.location.pathname);
      }

    } catch (error) {
      console.error('Error fetching chat response:', error);
      const errorMessage: Message = {
        text: 'Sorry, I seem to be having trouble connecting. Please try again later.',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  }, [processedMessages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSend(input);
    setInput('');
  };

  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Handle URL parameter from external page
  useEffect(() => {
    if (hasProcessedUrlMessage) return;

    console.log('=== URL DEBUGGING ===');
    console.log('Current URL:', window.location.href);
    console.log('Search params:', window.location.search);
    console.log('Pathname:', window.location.pathname);

    // Use native URLSearchParams to ensure we get the URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    const messageFromUrl = urlParams.get('message');

    console.log('All URL params:', Object.fromEntries(urlParams));
    console.log('Message from URL:', messageFromUrl);

    if (messageFromUrl) {
      const decodedMessage = decodeURIComponent(messageFromUrl);
      console.log('Decoded message:', decodedMessage);
      console.log('About to send message to API...');
      
      setHasProcessedUrlMessage(true);
      
      // Add a small delay to ensure the component is fully mounted
      setTimeout(() => {
        handleSend(decodedMessage);
      }, 100);
    } else {
      console.log('No message parameter found in URL');
    }
  }, [handleSend, hasProcessedUrlMessage]);

  return (
    <div className={styles.chat}>
      <div className={styles.chatHeader}>
        <button className={styles.menuButton} onClick={onMenuClick}>
          <FiMenu />
        </button>
        Chat with Ndu
      </div>
      <div className={styles.content}>
        <div className={styles.messages}>
          {messages.length === 0 ? (
            <div className={styles.welcome}>
              <h1>Welcome!</h1>
              <p>Your friendly assistant for the API Conference 2025 in Lagos. Ask me about speakers, schedules, and more!</p>
              <div className={styles.promptSuggestions}>
                <button className={styles.promptButton} onClick={() => handleSend('Who are the main speakers?')}>
                  Who are the main speakers?
                </button>
                <button className={styles.promptButton} onClick={() => handleSend('What is the conference schedule?')}>
                  What is the conference schedule?
                </button>
                <button className={styles.promptButton} onClick={() => handleSend('How do I get to the venue?')}>
                  How do I get to the venue?
                </button>
              </div>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`${styles.message} ${
                  msg.sender === 'user' ? styles.user : styles.bot
                }`}
              >
                <div className={styles.messageContent}>
                  {msg.sender === 'bot' ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.text}
                    </ReactMarkdown>
                  ) : (
                    msg.text
                  )}
                </div>
                <div className={styles.timestamp}>{msg.timestamp}</div>
              </div>
            ))
          )}
          {isTyping && (
            <div className={`${styles.message} ${styles.bot} ${styles.typing}`}>
              <TypingIndicator />
              <span>Ndu is typing...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className={styles.inputArea}>
        <form onSubmit={handleSubmit} className={styles.inputForm}>
          <input
            type="text"
            className={styles.inputField}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask something..."
          />
          <button type="submit" className={styles.sendButton}>
            <FiSend />
          </button>
        </form>
      </div>
    </div>
  );
};

export default Chat;