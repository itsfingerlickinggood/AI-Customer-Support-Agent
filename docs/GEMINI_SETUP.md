# Google Gemini API Setup Guide

This guide will help you set up Google Gemini API for the AI Customer Support Agent.

## Step 1: Access Google AI Studio

1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Sign in with your Google account
3. Accept the terms of service if prompted

## Step 2: Create API Key

1. Click on "Get API Key" or navigate to the API keys section
2. Click "Create API Key"
3. Choose "Create API key in new project" (recommended) or select an existing project
4. Copy the generated API key immediately (you won't be able to see it again)

## Step 3: Configure Environment

Add the API key to your `.env` file in the backend directory:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

Replace `your_actual_gemini_api_key_here` with your actual API key.

## Step 4: Verify Setup

1. Restart your backend server
2. Send a test message through the chat interface
3. Check the logs to see if Gemini API responses are being generated

## API Usage and Limits

### Free Tier Limits
- 60 requests per minute
- 1,500 requests per day
- Rate limits may apply

### Pricing (as of current date)
- Free tier available for development and testing
- Pay-as-you-go pricing for production use
- Check [Google AI Studio pricing](https://makersuite.google.com/pricing) for current rates

## Available Models

The application uses `gemini-1.5-flash` by default, which offers:
- Fast responses
- Good performance for customer support tasks
- Cost-effective for high-volume usage

### Other Available Models:
- `gemini-1.5-pro`: Higher quality responses, slower, more expensive
- `gemini-1.0-pro`: Legacy model, good performance

To change the model, update the `model_name` in `backend/app/gemini_service.py`:

```python
self.model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",  # Change this line
    # ... rest of configuration
)
```

## Safety Settings

The application includes safety settings to filter harmful content:

- Harassment: BLOCK_MEDIUM_AND_ABOVE
- Hate Speech: BLOCK_MEDIUM_AND_ABOVE
- Sexually Explicit: BLOCK_MEDIUM_AND_ABOVE
- Dangerous Content: BLOCK_MEDIUM_AND_ABOVE

These can be adjusted in `backend/app/gemini_service.py` if needed.

## Configuration Options

### Response Parameters

You can adjust the AI response behavior by modifying the generation config:

```python
generation_config={
    "temperature": 0.7,        # Creativity (0.0-1.0)
    "top_p": 0.8,             # Nucleus sampling
    "top_k": 40,              # Top-k sampling
    "max_output_tokens": 1024, # Maximum response length
}
```

### Temperature Settings:
- **0.0-0.3**: More deterministic, consistent responses
- **0.4-0.7**: Balanced creativity and consistency (recommended for customer support)
- **0.8-1.0**: More creative but less predictable responses

## Troubleshooting

### Common Issues:

**1. API Key Authentication Error**
```
Error: 401 Unauthorized
```
- Verify your API key is correct
- Make sure you copied the key completely
- Check if the key has been disabled or expired

**2. Rate Limit Exceeded**
```
Error: 429 Too Many Requests
```
- You've exceeded the API rate limits
- Wait before making more requests
- Consider upgrading to paid tier for higher limits

**3. Safety Filter Blocking**
```
Response blocked by safety filters
```
- The AI detected potentially harmful content
- Adjust safety settings if appropriate
- Rephrase the input to avoid triggering filters

**4. Model Not Found**
```
Error: 404 Model not found
```
- Check the model name spelling
- Verify the model is available in your region
- Try using a different model

### Getting Better Responses

**1. Improve Prompting:**
- Be specific about the desired response format
- Provide context about the customer support domain
- Include examples of good responses

**2. Use System Instructions:**
- The application includes a system prompt for customer support
- Customize it in `backend/app/gemini_service.py` for your specific needs

**3. Conversation Context:**
- The app automatically includes recent conversation history
- This helps maintain context across multiple turns

## Best Practices

### 1. API Key Security
- Never commit API keys to version control
- Use environment variables
- Rotate keys periodically
- Restrict API key usage to specific IPs if possible

### 2. Error Handling
- Always handle API errors gracefully
- Provide fallback responses for users
- Log errors for debugging but don't expose details to users

### 3. Performance Optimization
- Cache common responses where appropriate
- Use shorter context windows for faster responses
- Consider using the faster models for real-time chat

### 4. Content Moderation
- Keep safety settings enabled
- Monitor conversations for quality
- Have escalation paths to human agents

## Advanced Configuration

### Custom System Prompts

Edit the system prompt in `backend/app/gemini_service.py`:

```python
self.system_prompt = """You are a helpful AI customer support agent for [YOUR COMPANY]. 

Your role is to:
1. Provide friendly, professional responses
2. Help customers with [SPECIFIC PRODUCTS/SERVICES]
3. Escalate complex issues to human agents
4. Follow company policies and guidelines

Always be helpful, accurate, and professional."""
```

### Adding Context from Knowledge Base

To integrate with a knowledge base, modify the `generate_response` method to include relevant context:

```python
# Add relevant context from your knowledge base
knowledge_context = self.get_relevant_context(user_message)
context_messages.append(f"Context: {knowledge_context}")
```

## Monitoring and Analytics

Consider implementing:
- Response time tracking
- User satisfaction ratings
- Conversation completion rates
- API usage monitoring
- Error rate tracking

## Getting Help

- [Google AI Studio Documentation](https://makersuite.google.com/docs)
- [Gemini API Reference](https://ai.google.dev/docs)
- [Google Cloud Support](https://cloud.google.com/support)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-gemini)