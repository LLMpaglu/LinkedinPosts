import openai
import os

# Get user input
image_path = "" # enter the base image file path 
prompt = "" # enter the custom prompt instructions 
api_key = "" # Enter the api key 

if not api_key:
    raise ValueError("OpenAI API key is required.")

openai.api_key = api_key

# Open the image file
try:
    with open(image_path, "rb") as image_file:
        response = openai.Image.create_edit(
            image=image_file,
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
except Exception as e:
    print(f"Error sending request: {e}")
    exit(1)

# Get the URL of the generated image
try:
    image_url = response['data'][0]['url']
    print(f"Generated image URL: {image_url}")

    # Download and save the image
    import requests
    img_data = requests.get(image_url).content
    output_path = "generated_image.png"
    with open(output_path, 'wb') as handler:
        handler.write(img_data)
    print(f"Generated image saved as {output_path}")
except Exception as e:
    print(f"Error processing response: {e}")
