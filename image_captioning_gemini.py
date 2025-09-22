import os
import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from google import genai
from google.genai import types


def generate(img_data):
    """
    Generate caption for an image using Gemini Flash Lite
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please export it or add it to a .env file.")

        client = genai.Client(
            api_key=api_key,
        )

        model = "gemini-2.5-flash-lite"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_bytes(data=img_data, mime_type="image/png"),
                    types.Part.from_text(text="Describe the image in a few words."),
                ],
            ),
        ]
       
        generate_content_config = types.GenerateContentConfig(
            thinking_config = types.ThinkingConfig(
                thinking_budget=0,
            ),
            
        )

        # Collect all chunks to get the complete response
        full_response = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                full_response += chunk.text
        return full_response
    except Exception as e:
        return f"Error generating caption: {e}"

if __name__ == "__main__":

    # URL of the page to scrape
    url = "https://en.wikipedia.org/wiki/IBM"

    # Download the page with proper headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all img elements
    img_elements = soup.find_all('img')

    # Open a file to write the captions
    with open("captions.txt", "w") as caption_file:
        # Iterate over each img element
        for img_element in img_elements:
            img_url = img_element.get('src')

            # Skip if the image is an SVG or too small (likely an icon)
            if 'svg' in img_url or '1x1' in img_url:
                continue

            # Correct the URL if it's malformed
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif not img_url.startswith('http://') and not img_url.startswith('https://'):
                continue  # Skip URLs that don't start with http:// or https://

            try:
                # Download the image
                response = requests.get(img_url, headers=headers)
                # Convert the image data to a PIL Image
                raw_image = Image.open(BytesIO(response.content))
                if raw_image.size[0] * raw_image.size[1] < 400:  # Skip very small images
                    continue

                raw_image = raw_image.convert('RGB')

                # Convert PIL image to bytes for Gemini
                img_buffer = BytesIO()
                raw_image.save(img_buffer, format='PNG')
                img_data = img_buffer.getvalue()
                
                # Generate a caption for the image using Gemini
                caption = generate(img_data)

                # Write the caption to the file, prepended by the image URL
                caption_file.write(f"{img_url}:\n {caption}\n")
                
            except Exception as e:
                print(f"Error processing image {img_url}: {e}")
                continue