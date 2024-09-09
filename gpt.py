from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the Google Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key is missing. Please set GOOGLE_API_KEY in your .env file.")

genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    """Send a message to the Gemini model and get the response."""
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        print(f"An error occurred while getting a response: {e}")
        return None

def format_response(response):
    """Extract and format the content from the GenerateContentResponse object."""
    if response:
        # Try to access common attributes or methods of the response object
        formatted_response = ""
        for chunk in response:
            # Check the type of chunk or available attributes
            if hasattr(chunk, 'text'):
                formatted_response += chunk.text
            elif isinstance(chunk, str):
                formatted_response += chunk
            else:
                # If the response contains objects that are not strings or do not have 'text'
                print(f"Unexpected response chunk type: {type(chunk)}")
        return formatted_response
    return "No valid response received."

def main():
    print("Welcome to the Google Gemini chatbot! Type 'exit' to quit.")

    while True:
        input_text = input('Enter your question: ')

        if input_text.lower() == 'exit':
            print("Goodbye!")
            break

        # Simple filter to prevent unwanted content
        filtered_words = ["illegal", "hack", "pirate", "nudity", "porn"]
        if any(word in input_text.lower() for word in filtered_words):
            print("Sorry, I can't assist you with that information. 😟")
        else:
            response = get_gemini_response(input_text)
            if response:
                formatted_response = format_response(response)
                print("\nResponse:\n")
                print(formatted_response)
            else:
                print("No response received from the model.")

if __name__ == "__main__":
    main()
