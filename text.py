import openai
from gtts import gTTS
import os
from dotenv import load_dotenv
import sys
import re
import tavily

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY is missing from environment variables.")
    sys.exit(1)

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = tavily.TavilyClient(api_key=TAVILY_API_KEY)


# Define the positions for the conversation (Pro or Contra)
class Position:
    PRO = 0
    CON = 1


# Function to read prompt files and handle file-related errors
def read_prompt_file(file_path):
    try:
        # Open and read the content of the prompt file
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        # Handle case where the file is not found
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    except PermissionError:
        # Handle case where there are permission issues while reading the file
        print(f"Error: Permission denied while reading {file_path}.")
        sys.exit(1)
    except Exception as e:
        # Handle any unexpected errors
        print(f"Unexpected error while reading {file_path}: {e}")
        sys.exit(1)


# Function to get the first 10 alphanumeric characters of the "thema"
def get_file_name_from_thema(thema):
    # Remove non-alphanumeric characters and get the first 10 characters
    alphanumeric_thema = re.sub(r"[^a-zA-Z0-9]", "", thema)
    return alphanumeric_thema[:10]  # Return up to 10 characters


# Main function to handle the conversation flow and saving the output
def main():
    conversation = []  # List to hold the conversation
    current_position = Position.PRO  # Start with the "Pro" position

    # Prompt the user to input the topic ("thema") and ensure it's not empty
    try:
        thema = input("Thema: ")
        if not thema:
            raise ValueError("Thema cannot be empty.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Prompt the user to input the number of iterations for conversation
    try:
        # Multiply by 2 because the conversation alternates between "Pro" and "Contra"
        iterations = int(input("Iterations: ")) * 2
        if iterations <= 0:
            raise ValueError("Iterations must be a positive integer.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    context = tavily_client.get_search_context(thema)
    print(f"Kontext aus dem Internet:\n{context}")
    print("---")

    # Loop through the number of iterations to generate the conversation
    for i in range(iterations):
        # Determine which prompt file to use based on the iteration
        if i == 0:
            prompt_file = "prompt_start.txt"  # First iteration uses "start" prompt
        elif i < iterations - 2:
            prompt_file = "prompt_mid.txt"  # Middle iterations use "mid" prompt
        else:
            prompt_file = "prompt_end.txt"  # Last iteration uses "end" prompt

        # Read the system prompt from the respective file and replace placeholders
        system_prompt = (
            read_prompt_file(prompt_file)
            .replace(
                "{{procontra}}", "pro" if current_position == Position.PRO else "contra"
            )
            .replace("{{thema}}", thema)
            .replace("{{context}}", context)
        )

        # Prepare the conversation history for OpenAI API request
        conversation_openai = []
        for i, message in enumerate(conversation):
            # Determine if the current message is from the user or assistant
            message_author_is_different = (len(conversation) - i) % 2
            conversation_openai.append(
                {
                    "role": "user" if message_author_is_different else "assistant",
                    "content": message,
                }
            )

        # Call OpenAI API to generate a response based on the conversation so far
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},  # System prompt
                    *conversation_openai,  # The current conversation history
                ],
            )
            # Extract the message content from the API response
            message_content = response.choices[0].message.content
            print(message_content)  # Print the response for debugging
            print("---")
            conversation.append(message_content)  # Add the response to the conversation
            # Toggle the current position between "Pro" and "Contra"
            current_position = (
                Position.CON if current_position == Position.PRO else Position.PRO
            )
        except openai.error.OpenAIError as e:
            # Handle errors related to OpenAI API
            print(f"Error with OpenAI API: {e}")
            sys.exit(1)
        except Exception as e:
            # Handle unexpected errors during API calls
            print(f"Unexpected error during API call: {e}")
            sys.exit(1)

    # Ensure the directory to save the file exists
    output_dir = "generated_text"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the directory if it doesn't exist

    # Generate the file name based on the "thema"
    file_name = get_file_name_from_thema(thema)

    # Serialize the conversation to a text file in the "generated_text" directory
    try:
        output_path = os.path.join(
            output_dir, f"{file_name}.txt"
        )  # Construct the file path
        with open(output_path, "w") as f:
            f.write(repr(conversation))  # Save the conversation history to the file
        print(f"File saved to {output_path}")  # Inform the user where the file is saved
    except PermissionError:
        # Handle case where there are permission issues while saving the file
        print(f"Error: Permission denied when saving {file_name}.txt.")
        sys.exit(1)
    except Exception as e:
        # Handle unexpected errors while saving the file
        print(f"Unexpected error while saving {file_name}.txt: {e}")
        sys.exit(1)


# Ensure the main function runs when the script is executed
if __name__ == "__main__":
    try:
        main()  # Call the main function to start the program
    except Exception as e:
        # Handle any unexpected errors that occur during execution
        print(f"Unexpected error: {e}")
        sys.exit(1)
