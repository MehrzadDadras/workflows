import os
import openai
import time
import logging

# Configure logging
logging.basicConfig(filename='outline_generation.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# Access the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logging.error("API key is not set in environment variables.")
    raise ValueError("API key is not set in environment variables.")
openai.api_key = api_key

# Define the prompt for the API call
prompt = "Write an outline for a chapter on effective scheduling in construction project management."

# Function to make the API call
def get_outline(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500  # Adjust the number of tokens if necessary
        )
        logging.info("API call successful.")
        return response['choices'][0]['message']['content'].strip()
    except openai.error.RateLimitError as e:
        logging.warning(f"Rate limit exceeded: {e}")
        time.sleep(60)  # Wait for 60 seconds before retrying
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500  # Adjust the number of tokens if necessary
        )
        logging.info("API call successful after retry.")
