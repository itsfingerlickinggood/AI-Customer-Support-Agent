import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';

// Mock the ChatWidget component
jest.mock('../ChatWidget', () => {
  return function MockChatWidget() {
    return <div data-testid="chat-widget">Chat Widget</div>;
  };
});

describe('App', () => {
  test('renders main heading', () => {
    render(<App />);
    
    expect(screen.getByText('AI Customer Support Agent')).toBeInTheDocument();
  });

  test('renders welcome message', () => {
    render(<App />);
    
    expect(screen.getByText('Welcome to our intelligent customer support system')).toBeInTheDocument();
  });

  test('renders all feature cards', () => {
    render(<App />);
    
    expect(screen.getByText('🤖 AI-Powered')).toBeInTheDocument();
    expect(screen.getByText('💬 Contextual Memory')).toBeInTheDocument();
    expect(screen.getByText('⚡ Real-time')).toBeInTheDocument();
  });

  test('renders feature descriptions', () => {
    render(<App />);
    
    expect(screen.getByText('Get instant responses from our intelligent AI assistant')).toBeInTheDocument();
    expect(screen.getByText('Our AI remembers your conversation for better assistance')).toBeInTheDocument();
    expect(screen.getByText('Fast responses to help you resolve issues quickly')).toBeInTheDocument();
  });

  test('renders call to action', () => {
    render(<App />);
    
    expect(screen.getByText('Need help? Click the chat button to start a conversation!')).toBeInTheDocument();
  });

  test('renders chat widget', () => {
    render(<App />);
    
    expect(screen.getByTestId('chat-widget')).toBeInTheDocument();
  });
});