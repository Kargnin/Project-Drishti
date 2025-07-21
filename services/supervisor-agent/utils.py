from dotenv import load_dotenv
load_dotenv()
from groq import Groq
import base64
import os
from prompts import *

groq_client = Groq(api_key = os.environ.get("Groq_Cloud_API_Key"))

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "images/normal2.jpg"

base64_image = encode_image(image_path)

chat_completion = groq_client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": IMAGE_ANALYSIS_PROMPT},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
    model="meta-llama/llama-4-scout-17b-16e-instruct",
)

print(chat_completion.choices[0].message.content)

