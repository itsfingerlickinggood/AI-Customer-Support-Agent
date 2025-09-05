import google.generativeai as genai
from app.config import settings
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.use_mock = True  # Start in mock mode for demo
        
        # Only try to initialize Gemini if API key looks valid  
        if settings.gemini_api_key != "demo_key_for_testing":
            try:
                # Configure Gemini API
                genai.configure(api_key=settings.gemini_api_key)
                
                # Initialize the model
                self.model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.8,
                        "top_k": 40,
                        "max_output_tokens": 1024,
                    },
                    safety_settings=[
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                        },
                        {
                            "category": "HARM_CATEGORY_HATE_SPEECH",
                            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                        },
                        {
                            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                        },
                        {
                            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                        }
                    ]
                )
                self.use_mock = False
                logger.info("Gemini API configured successfully")
            except Exception as e:
                logger.warning(f"Could not configure Gemini API: {str(e)}. Using mock responses.")
                self.use_mock = True
        else:
            logger.info("Using demo/mock mode for Gemini (no real API key configured)")
        
        # System prompt for customer support agent
        self.system_prompt = """You are a helpful AI customer support agent. Your role is to:

1. Provide friendly, professional, and helpful responses
2. Ask clarifying questions when needed
3. Offer practical solutions to customer problems
4. Be empathetic and understanding
5. Keep responses concise but informative
6. If you don't know something, admit it and offer to escalate to a human agent

Always maintain a helpful and positive tone. Focus on solving the customer's problem efficiently."""

    async def generate_response(self, user_message: str, conversation_history: List[Dict[str, Any]] = None) -> str:
        """Generate a response using Gemini API with conversation context"""
        if self.use_mock:
            return self._generate_mock_response(user_message, conversation_history)
        
        try:
            # Build conversation context
            context_messages = []
            
            # Add system prompt
            context_messages.append(f"System: {self.system_prompt}")
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages for context
                    role = "User" if msg.get("role") == "user" else "Assistant"
                    content = msg.get("content", "")
                    context_messages.append(f"{role}: {content}")
            
            # Add current user message
            context_messages.append(f"User: {user_message}")
            context_messages.append("Assistant:")
            
            # Create the full prompt
            full_prompt = "\n".join(context_messages)
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                logger.warning("Empty response from Gemini API")
                return "I apologize, but I'm having trouble generating a response right now. Could you please try again or rephrase your question?"
                
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            
            # Fallback to mock
            self.use_mock = True
            return self._generate_mock_response(user_message, conversation_history)

    async def generate_simple_response(self, user_message: str) -> str:
        """Generate a simple response without conversation context"""
        if self.use_mock:
            return self._generate_mock_simple_response(user_message)
        
        try:
            # Create a simple prompt
            prompt = f"{self.system_prompt}\n\nUser: {user_message}\nAssistant:"
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return "Thank you for your message. How can I help you today?"
                
        except Exception as e:
            logger.error(f"Error in simple Gemini response: {str(e)}")
            # Fallback to mock
            self.use_mock = True
            return self._generate_mock_simple_response(user_message)
    
    def _generate_mock_response(self, user_message: str, conversation_history: List[Dict[str, Any]] = None) -> str:
        """Generate a mock response for testing/demo purposes"""
        mock_responses = [
            f"Thank you for contacting our support team! I understand you mentioned: '{user_message}'. I'm here to help you resolve this issue.",
            f"I see you're asking about '{user_message}'. Let me provide you with some assistance on this matter.",
            f"Thanks for reaching out! Regarding '{user_message}', I'd be happy to help. Could you provide a bit more detail about your specific situation?",
            f"I appreciate you contacting us about '{user_message}'. Based on your message, I can offer some guidance to help resolve this.",
            f"Hello! I've received your message about '{user_message}'. I'm here to provide support and find the best solution for you."
        ]
        
        # Use conversation history length to vary responses
        history_length = len(conversation_history) if conversation_history else 0
        response_index = history_length % len(mock_responses)
        
        return mock_responses[response_index]
    
    def _generate_mock_simple_response(self, user_message: str) -> str:
        """Generate a simple mock response"""
        return f"Thank you for your message: '{user_message}'. I'm here to help! Could you please tell me more about what you need assistance with?"

# Global instance
gemini_service = GeminiService()