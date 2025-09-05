# Appwrite Setup Guide

This guide will help you set up Appwrite for the AI Customer Support Agent.

## Step 1: Create Appwrite Account

1. Go to [Appwrite Cloud](https://appwrite.io/)
2. Sign up for a free account
3. Verify your email address

## Step 2: Create a New Project

1. Click "Create Project"
2. Enter project name: "AI Customer Support"
3. Enter project ID: "ai-customer-support" (or any unique ID)
4. Select your region
5. Click "Create"

## Step 3: Set Up Database

1. Navigate to "Databases" in the left sidebar
2. Click "Create Database"
3. Name: "main"
4. Database ID: "main"
5. Click "Create"

## Step 4: Create Collections

### Create Conversations Collection

1. In the "main" database, click "Create Collection"
2. Name: "conversations"
3. Collection ID: "conversations"
4. Click "Create"

**Add Attributes:**
1. Click "Create Attribute" → "String"
   - Key: `session_id`
   - Size: 255
   - Required: Yes
   - Default: (leave empty)

2. Click "Create Attribute" → "DateTime"
   - Key: `created_at`
   - Required: Yes
   - Default: (leave empty)

3. Click "Create Attribute" → "DateTime"
   - Key: `updated_at`
   - Required: Yes
   - Default: (leave empty)

### Create Messages Collection

1. Click "Create Collection"
2. Name: "messages"
3. Collection ID: "messages"
4. Click "Create"

**Add Attributes:**
1. Click "Create Attribute" → "String"
   - Key: `session_id`
   - Size: 255
   - Required: Yes

2. Click "Create Attribute" → "String"
   - Key: `role`
   - Size: 50
   - Required: Yes
   - Default: (leave empty)

3. Click "Create Attribute" → "String"
   - Key: `content`
   - Size: 10000
   - Required: Yes
   - Default: (leave empty)

4. Click "Create Attribute" → "DateTime"
   - Key: `timestamp`
   - Required: Yes
   - Default: (leave empty)

## Step 5: Set Up API Key

1. Go to "Settings" → "API Keys"
2. Click "Create API Key"
3. Name: "AI Customer Support Backend"
4. Scopes:
   - Select "Database"
   - Under Database, select:
     - `databases.read`
     - `databases.write`
     - `documents.read`
     - `documents.write`
5. Click "Create"
6. Copy the generated API key

## Step 6: Configure Permissions (Optional)

For production, you may want to set up proper permissions:

### Conversations Collection Permissions:
- Read: `users`
- Write: `users`
- Create: `users`
- Update: `users`
- Delete: `users`

### Messages Collection Permissions:
- Read: `users`
- Write: `users`
- Create: `users`
- Update: `users`
- Delete: `users`

## Step 7: Environment Configuration

Add the following to your `.env` file in the backend directory:

```env
# Appwrite Configuration
APPWRITE_PROJECT_ID=your_project_id_here
APPWRITE_API_KEY=your_api_key_here
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_DATABASE_ID=main
APPWRITE_CONVERSATIONS_COLLECTION_ID=conversations
APPWRITE_MESSAGES_COLLECTION_ID=messages
```

Replace:
- `your_project_id_here` with your actual project ID
- `your_api_key_here` with your actual API key

## Step 8: Test Connection

1. Restart your backend server
2. Check the logs to see if it connects to Appwrite successfully
3. Send a test message through the chat interface
4. Verify data appears in your Appwrite database

## Troubleshooting

### Common Issues:

**1. Authentication Error**
- Verify your API key is correct
- Make sure the API key has the right permissions

**2. Collection Not Found**
- Check collection IDs match exactly
- Ensure collections exist in the correct database

**3. Attribute Validation Error**
- Verify all required attributes are created
- Check attribute types match the schema

**4. Network Connection Error**
- Ensure your server can reach cloud.appwrite.io
- Check firewall settings if running on a server

### Getting Help

- [Appwrite Documentation](https://appwrite.io/docs)
- [Appwrite Discord Community](https://discord.gg/GSeTUeA)
- [GitHub Issues](https://github.com/appwrite/appwrite/issues)

## Self-Hosted Appwrite (Advanced)

If you prefer to self-host Appwrite:

1. Follow the [Appwrite installation guide](https://appwrite.io/docs/installation)
2. Update the `APPWRITE_ENDPOINT` in your `.env` file to your self-hosted URL
3. Configure your self-hosted instance following the same steps above

## Security Best Practices

1. **Use Environment Variables**: Never commit API keys to version control
2. **Limit API Key Permissions**: Only grant necessary scopes
3. **Set Up Proper Authentication**: In production, implement user authentication
4. **Configure CORS**: Restrict API access to your domain only
5. **Regular Key Rotation**: Periodically rotate API keys for security