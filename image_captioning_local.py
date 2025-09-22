import os
from dotenv import load_dotenv
import glob
from PIL import Image


from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please set it in your environment or .env file.")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)

# Specify the directory where your images are
image_dir = "./fotoss"
image_exts = ["jpg", "jpeg", "png"]  # specify the image file extensions to search for

# Open a file to write the captions
with open("captions.txt", "w") as caption_file:
    # Iterate over each image file in the directory
    for image_ext in image_exts:
        for img_path in glob.glob(os.path.join(image_dir, f"*.{image_ext}")):
            # Load your image
            raw_image = Image.open(img_path).convert('RGB')

            
            inputs = processor(raw_image, return_tensors="pt")

            # Generate a caption for the image
            out = model.generate(**inputs, max_new_tokens=50)

            # Decode the generated tokens to text
            caption = processor.decode(out[0], skip_special_tokens=True)

            # Write the caption to the file, prepended by the image file name
            caption_file.write(f"{os.path.basename(img_path)}: {caption}\n")