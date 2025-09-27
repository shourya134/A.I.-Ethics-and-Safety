# 🤖 Terminal ChatGPT Setup

## Quick Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key:**
   ```bash
   # Option 1: Environment variable
   export OPENAI_API_KEY="your-api-key-here"

   # Option 2: Create .env file
   cp env_example.txt .env
   # Edit .env and add your API key
   ```

3. **Run ChatGPT in terminal:**
   ```bash
   # Interactive mode
   python src/terminal_chatgpt.py

   # Or use the launcher script
   ./scripts/chatgpt

   # Single message mode
   python src/terminal_chatgpt.py --message "Hello, how are you?"

   # With specific model
   python src/terminal_chatgpt.py --model gpt-4
   ```

## Features

- 💬 **Interactive chat mode** - Persistent conversation
- 🔄 **Model switching** - Switch between GPT models
- 💾 **Save/load conversations** - Keep chat history
- 🧹 **Clear history** - Start fresh conversations
- ⚡ **Single message mode** - Quick one-off queries

## Commands

While in interactive mode:
- `/clear` - Clear conversation history
- `/save` - Save conversation to JSON file
- `/load <filename>` - Load previous conversation
- `/model <model-name>` - Switch GPT model
- `/quit` or `/exit` - Exit the chat

## Usage Examples

```bash
# Basic interactive chat
./scripts/chatgpt

# Quick question
./scripts/chatgpt --message "Explain quantum computing"

# Use GPT-4 with system prompt
./scripts/chatgpt --model gpt-4 --message "Write a Python function" --system "You are a senior Python developer"
```

## API Key Setup

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys) and set it as:

```bash
export OPENAI_API_KEY="sk-proj-your-key-here"
```

## File Structure

- `src/terminal_chatgpt.py` - Main ChatGPT interface
- `scripts/chatgpt` - Executable launcher script
- `data/` - Saved conversations (auto-created)
- `.env` - Your API key configuration

**🎉 You're ready to chat with ChatGPT in your terminal!**