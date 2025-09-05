import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChatWidget from '../ChatWidget';

// Mock fetch for API calls
global.fetch = jest.fn();

// Mock scrollIntoView
Object.defineProperty(window.Element.prototype, 'scrollIntoView', {
  writable: true,
  value: jest.fn(),
});

describe('ChatWidget', () => {
  beforeEach(() => {
    // Reset fetch mock before each test
    (fetch as jest.Mock).mockClear();
  });

  test('renders chat trigger button initially', () => {
    render(<ChatWidget />);
    
    expect(screen.getByText('Need help?')).toBeInTheDocument();
    expect(screen.getByText('💬')).toBeInTheDocument();
  });

  test('opens chat widget when trigger is clicked', () => {
    render(<ChatWidget />);
    
    const trigger = screen.getByText('Need help?');
    fireEvent.click(trigger);
    
    expect(screen.getByText('Customer Support')).toBeInTheDocument();
    expect(screen.getByText('👋 Hi! I\'m your AI customer support assistant. How can I help you today?')).toBeInTheDocument();
  });

  test('displays message input and send button when opened', () => {
    render(<ChatWidget />);
    
    const trigger = screen.getByText('Need help?');
    fireEvent.click(trigger);
    
    expect(screen.getByPlaceholderText('Type your message...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '➤' })).toBeInTheDocument();
  });

  test('enables send button when message is typed', () => {
    render(<ChatWidget />);
    
    const trigger = screen.getByText('Need help?');
    fireEvent.click(trigger);
    
    const messageInput = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: '➤' });
    
    expect(sendButton).toBeDisabled();
    
    fireEvent.change(messageInput, { target: { value: 'Hello' } });
    
    expect(sendButton).not.toBeDisabled();
  });

  test('sends message when send button is clicked', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Thank you for your message',
        session_id: 'test-session-id',
        timestamp: new Date().toISOString()
      })
    });

    render(<ChatWidget />);
    
    const trigger = screen.getByText('Need help?');
    fireEvent.click(trigger);
    
    const messageInput = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: '➤' });
    
    fireEvent.change(messageInput, { target: { value: 'Hello, I need help' } });
    fireEvent.click(sendButton);
    
    expect(fetch).toHaveBeenCalledWith('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: 'Hello, I need help',
        session_id: null,
      }),
    });

    await waitFor(() => {
      expect(screen.getByText('Hello, I need help')).toBeInTheDocument();
      expect(screen.getByText('Thank you for your message')).toBeInTheDocument();
    });
  });

  test('clears chat when clear button is clicked', async () => {
    (fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Test response',
        session_id: 'test-session-id',
        timestamp: new Date().toISOString()
      })
    });

    render(<ChatWidget />);
    
    const trigger = screen.getByText('Need help?');
    fireEvent.click(trigger);
    
    // Send a message first
    const messageInput = screen.getByPlaceholderText('Type your message...');
    fireEvent.change(messageInput, { target: { value: 'Test message' } });
    fireEvent.keyPress(messageInput, { key: 'Enter', code: 'Enter', charCode: 13 });
    
    await waitFor(() => {
      expect(screen.getByText('Test message')).toBeInTheDocument();
    });
    
    // Clear the chat
    const clearButton = screen.getByTitle('Clear chat');
    fireEvent.click(clearButton);
    
    expect(screen.queryByText('Test message')).not.toBeInTheDocument();
    expect(screen.getByText('👋 Hi! I\'m your AI customer support assistant. How can I help you today?')).toBeInTheDocument();
  });

  test('closes chat when close button is clicked', () => {
    render(<ChatWidget />);
    
    const trigger = screen.getByText('Need help?');
    fireEvent.click(trigger);
    
    expect(screen.getByText('Customer Support')).toBeInTheDocument();
    
    const closeButton = screen.getByTitle('Close chat');
    fireEvent.click(closeButton);
    
    expect(screen.queryByText('Customer Support')).not.toBeInTheDocument();
    expect(screen.getByText('Need help?')).toBeInTheDocument();
  });

  test('handles API error gracefully', async () => {
    (fetch as jest.Mock).mockRejectedValueOnce(new Error('API Error'));

    render(<ChatWidget />);
    
    const trigger = screen.getByText('Need help?');
    fireEvent.click(trigger);
    
    const messageInput = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: '➤' });
    
    fireEvent.change(messageInput, { target: { value: 'Test error handling' } });
    fireEvent.click(sendButton);
    
    await waitFor(() => {
      expect(screen.getByText('Sorry, I encountered an error. Please try again.')).toBeInTheDocument();
    });
  });
});