import React, { useState, useRef } from 'react';
import axios from 'axios'

function Chat() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');



    const handleSendMessage = (): void => {

    if (newMessage.trim() === '') {
      return; // Don't send empty messages
    }
    const newMessages: Message[] = [...messages, { text: newMessage, user: 'You' }];
    setMessages(newMessages);
    setNewMessage('');
  };

  const handleInputChange = (event) => {
    setNewMessage(event.target.value);
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`chat-message ${message.user === 'You' ? 'outgoing' : 'incoming'}`}>
            <span className="chat-username">Usuario:</span> {message.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          placeholder="Type your message..."
          value={newMessage}
          onChange={handleInputChange}
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
}

export default Chat;
