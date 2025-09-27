#!/usr/bin/env python3
"""
Terminal ChatGPT Interface
A simple command-line interface for interacting with OpenAI's GPT models.
"""

import os
import sys
import json
from typing import Optional, List, Dict
from datetime import datetime
import openai
from dotenv import load_dotenv

class TerminalChatGPT:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """Initialize the terminal ChatGPT interface."""
        load_dotenv()

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass api_key parameter.")

        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []

    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Send a message to ChatGPT and return the response."""
        try:
            messages = []

            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            # Add conversation history
            messages.extend(self.conversation_history)

            # Add current message
            messages.append({"role": "user", "content": message})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )

            assistant_response = response.choices[0].message.content

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})

            # Keep history manageable (last 20 messages)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]

            return assistant_response

        except Exception as e:
            return f"Error: {str(e)}"

    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
        print("🧹 Conversation history cleared.")

    def save_conversation(self, filename: Optional[str] = None):
        """Save the current conversation to a file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"

        filepath = os.path.join("data", filename)
        os.makedirs("data", exist_ok=True)

        with open(filepath, 'w') as f:
            json.dump({
                "model": self.model,
                "timestamp": datetime.now().isoformat(),
                "conversation": self.conversation_history
            }, f, indent=2)

        print(f"💾 Conversation saved to {filepath}")

    def load_conversation(self, filename: str):
        """Load a conversation from a file."""
        filepath = os.path.join("data", filename)

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.conversation_history = data.get("conversation", [])
                print(f"📂 Conversation loaded from {filepath}")
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in file: {filepath}")

    def interactive_mode(self):
        """Start an interactive chat session."""
        print("🤖 Terminal ChatGPT Interface")
        print("=" * 50)
        print(f"Model: {self.model}")
        print("Commands:")
        print("  /clear    - Clear conversation history")
        print("  /save     - Save conversation to file")
        print("  /load <file> - Load conversation from file")
        print("  /model <model> - Change model (gpt-3.5-turbo, gpt-4, etc.)")
        print("  /quit     - Exit the chat")
        print("=" * 50)

        while True:
            try:
                user_input = input("\n🧑 You: ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith('/'):
                    command_parts = user_input[1:].split(' ', 1)
                    command = command_parts[0].lower()

                    if command == 'quit' or command == 'exit':
                        print("👋 Goodbye!")
                        break
                    elif command == 'clear':
                        self.clear_history()
                        continue
                    elif command == 'save':
                        self.save_conversation()
                        continue
                    elif command == 'load' and len(command_parts) > 1:
                        self.load_conversation(command_parts[1])
                        continue
                    elif command == 'model' and len(command_parts) > 1:
                        self.model = command_parts[1]
                        print(f"🔄 Model changed to: {self.model}")
                        continue
                    else:
                        print("❌ Unknown command. Type /quit to exit.")
                        continue

                # Send message to ChatGPT
                print("🤖 ChatGPT: ", end="", flush=True)
                response = self.chat(user_input)
                print(response)

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break

def main():
    """Main function to run the terminal ChatGPT interface."""
    import argparse

    parser = argparse.ArgumentParser(description="Terminal ChatGPT Interface")
    parser.add_argument("--api-key", help="OpenAI API key")
    parser.add_argument("--model", default="gpt-3.5-turbo", help="GPT model to use")
    parser.add_argument("--message", help="Single message mode (non-interactive)")
    parser.add_argument("--system", help="System prompt for single message mode")

    args = parser.parse_args()

    try:
        chatgpt = TerminalChatGPT(api_key=args.api_key, model=args.model)

        if args.message:
            # Single message mode
            response = chatgpt.chat(args.message, system_prompt=args.system)
            print(response)
        else:
            # Interactive mode
            chatgpt.interactive_mode()

    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()