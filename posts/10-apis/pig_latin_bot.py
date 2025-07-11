from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def main():
    print("🐷 Welcome to the Pig Latin Chatbot! (Type 'quit' to exit)")
    print("-" * 50)
    
    # Store conversation history
    messages = [
        {"role": "system", "content": "Answer in pig latin."}
    ]
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Check for quit command
        if user_input.lower() == 'quit':
            print("Oodbye-gay! 🐷")
            break
        
    # Add user message to history
    messages.append({"role": "user", "content": user_input})
    

        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            stream=True
        )
        
        # Print assistant response
        print("Bot: ", end="", flush=True)
        full_response = ""
        
        # Stream the response
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        
        print()  # New line after response
        
        # Add assistant response to history
        messages.append({"role": "assistant", "content": full_response})
 

if __name__ == "__main__":
    main()