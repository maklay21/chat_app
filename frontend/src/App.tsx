import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

interface Message {
  text: string;
  sender: string;
  timestamp: string;
}

const API_BASE_URL = 'http://localhost:8000';

const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Загрузка сообщений при обновлении страницы
  useEffect(() => {
    fetchMessages();
  }, []);

  // Прокрутка к последнему сообщению
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const fetchMessages = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get(`${API_BASE_URL}/api/messages`);
      
      // Реверс сообщений из редис
      const reversedMessages = [...response.data.messages].reverse();
      setMessages(reversedMessages);
      
    } catch (error) {
    
      console.error('Error loading message:', error);
    } finally {
    
      setIsLoading(false);
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const newMessage: Message = {
      text: inputText,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    try {
      setMessages(prev => [...prev, newMessage]);
      setInputText('');

      await axios.post(`${API_BASE_URL}/api/messages`, newMessage);
      
      // Обновление списка сообщений с сервера
      await fetchMessages();
    } catch (error) {
      console.error('Error sending message:', error);
      
      fetchMessages();
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false
    });
  };

  return (
    <div className="chat-app">
      <div className="chat-container">
        {/* Заголовок чата */}
        <div className="chat-header">
          <div className="chat-header-info">
            <div className="chat-title">Hustlers Tech Agency</div>
            <div className="chat-members">1 member</div>
          </div>
        </div>

        {/* Область сообщений */}
        <div className="messages-container">
          {isLoading && messages.length === 0 ? (
            <div className="loading">Loading...</div>
          ) : (
            <>
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message ${message.sender === 'user' ? 'sent' : 'received'}`}
                >
                  <div className="message-content">
                    <div className="message-text">{message.text}</div>
                    <div className="message-time">
                      {formatTime(message.timestamp)}
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Строка ввода */}
        <form className="input-container" onSubmit={sendMessage}>
          <div className="input-wrapper">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Message"
              className="message-input"
            />
            <button type="submit" className="send-button">
              <svg width="24" height="24" viewBox="0 0 24 24">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" fill="currentColor"/>
              </svg>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default App;
