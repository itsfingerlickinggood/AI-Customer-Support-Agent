import React from 'react';
import ChatWidget from './ChatWidget';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Customer Support Agent</h1>
        <p>Welcome to our intelligent customer support system</p>
        <div className="features">
          <div className="feature">
            <h3>🤖 AI-Powered</h3>
            <p>Get instant responses from our intelligent AI assistant</p>
          </div>
          <div className="feature">
            <h3>💬 Contextual Memory</h3>
            <p>Our AI remembers your conversation for better assistance</p>
          </div>
          <div className="feature">
            <h3>⚡ Real-time</h3>
            <p>Fast responses to help you resolve issues quickly</p>
          </div>
        </div>
        <div className="cta">
          <p>Need help? Click the chat button to start a conversation!</p>
        </div>
      </header>
      <ChatWidget />
    </div>
  );
}

export default App;
