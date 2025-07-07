import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import styles from './Chat.module.css';
import TypingIndicator from './TypingIndicator';
import { FiSend } from 'react-icons/fi';

interface Message {
  text: string;
  sender: 'user' | 'bot';
  timestamp: string;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (messageToSend: string) => {
    if (!messageToSend.trim()) return;

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
          user_id: '12345', // Example user_id
          session_id: 'abcde', // Example session_id
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      const botMessage: Message = {
        text: result.data.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
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
  };

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

  return (
    <div className={styles.chat}>
      <div className={styles.chatHeader}>Chat with Ndu</div>
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