# OpenAI Image Editing Script

This script allows you to generate new images by sending a base image and a prompt to the OpenAI DALL·E API.

## Requirements
- Python 3.7+
- An OpenAI API key
- The base image must be a PNG file and less than 4MB

## Installation
1. Clone this repository or download the script.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the script:
   ```bash
   python OpenAI.py
   ```
2. Enter the path to your base PNG image when prompted.
3. Enter a prompt describing the desired change.
4. Enter your OpenAI API key (or set it as the `OPENAI_API_KEY` environment variable).

The generated image will be saved as `generated_image.png` in the current directory.

## Notes
- The script uses the OpenAI DALL·E API's image editing endpoint.
- Make sure your base image is a PNG and less than 4MB.
- For more information, see the [OpenAI Image API documentation](https://platform.openai.com/docs/guides/images/usage). 