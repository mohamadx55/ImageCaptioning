

import base64
import os
from google import genai
from google.genai import types

img_path = "image.png"

def generate():
    client = genai.Client(
        api_key="",
    )

    model = "gemini-2.5-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(data=open(img_path, "rb").read() , mime_type="image/png"),
                types.Part.from_text(text="Describe the image in a few words."),
            ],
        ),
    ]
   
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
        
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()


