"""This file will be responsible to get new names from OpenAI

Inputs: Prompt
functionality:
    1. send the prompt to openai get the names
    2. Split names into list of names got by the openAI
Output: List of Names




Output:
- A list of names that are generated based on the prompt.
"""

import openai
from helper_functions.utils import read_prompt
import os
from dotenv import load_dotenv
import re

# Load environment variables from the .env file
load_dotenv()

# Initialize the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


def normalize_words(words):
    normalized_words = []
    for word in words:
        normalized_word = re.sub(r"[^a-zA-Z0-9]", "", word).lower()
        normalized_words.append(normalized_word)
    return normalized_words


def name_finder(prompt: str) -> list:
    """
    Function to find names based on the provided prompt using OpenAI's API.

    Args:
        prompt (str): The prompt used to generate names.

    Returns:
        list: A list of names generated by the OpenAI API.
    """
    names = []
    try:
        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {"role": "user", "content": "Give me creative and catchy names."},
            ],
            temperature=1,
        )

        # Extract and process the response
        response_text = response.choices[0].message["content"].strip()

        if not response_text:
            print("No names generated.")
            return []

        # Process the response to get names
        name_suggestions = response_text.split("\n")
        names = [name for name in name_suggestions if name]
        names = normalize_words(names)

        if not names:
            print("No valid names found. Try adjusting the prompt or parameters.")

    except Exception as e:
        print(f"An error occurred: {e}")

    return names


# # Only for testing
# if __name__ == "__main__":
#     # Read the prompt from the external file
#     prompt = read_prompt("helper_functions/prompt.txt")

#     names = name_finder(prompt)

#     if names:
#         print("\nRecommended Names:")
#         for name in names:
#             print(name)
#     else:
#         print("No names were returned.")
