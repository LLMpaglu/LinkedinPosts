# AI Image Generation Suite

A comprehensive Python application suite for AI-powered image generation and editing. Features DALL-E image editing, GPT-4 Vision image generation, and advanced image masking capabilities.

*Made by Anant with ❤️*

## 🚀 Features

### 🎨 **DALL-E Image Editor** (`OpenAI.py`)
- ✅ **Image Editing**: Edit existing images with text prompts
- ✅ **Input Validation**: Validates image format (PNG), file size (<4MB), and file existence
- ✅ **Error Handling**: Comprehensive error handling for API issues and user input errors
- ✅ **User-Friendly**: Interactive prompts with retry logic for invalid inputs
- ✅ **Flexible API Key**: Support for both direct input and environment variable

### 🖼️ **GPT-4 Vision Image Generator** (`streamlit_app.py`)
- ✅ **Multi-Image Input**: Upload 1-4 reference images for generation
- ✅ **Vision Understanding**: Uses GPT-4 Vision to understand image content
- ✅ **Advanced Generation**: Creates new images based on multiple reference images
- ✅ **Web Interface**: Modern Streamlit UI with drag-and-drop upload
- ✅ **Multiple Formats**: Supports PNG, JPG, JPEG, GIF, WEBP (up to 20MB each)
- ✅ **Real-time Preview**: See uploaded images before generation
- ✅ **Direct Download**: Download generated images directly from the web interface

### 🎭 **AI Image Masking** (`image_masking_streamlit.py`)
- ✅ **Precise Masking**: Generate new content in specific masked areas
- ✅ **Dual Image Upload**: Upload base image and mask image separately
- ✅ **Quality Control**: Choose between standard and high quality output
- ✅ **Mask Guidelines**: Clear instructions for creating effective masks
- ✅ **Custom Output**: Specify custom output filenames
- ✅ **Visual Feedback**: Preview both base and mask images before processing

## Requirements

- Python 3.7+
- An OpenAI API key with access to:
  - DALL-E API (for image editing)
  - GPT-4 Vision API (for image generation)
- Image requirements:
  - **DALL-E Editor**: PNG format, <4MB
  - **GPT-4 Generator**: PNG/JPG/GIF/WEBP, <20MB each

## Installation

1. Clone this repository or download the files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 🌐 **GPT-4 Vision Image Generator**

Launch the modern web interface:
```bash
# Easy launcher
python run_image_generator.py

# Or direct Streamlit
streamlit run streamlit_app.py
```

**Features:**
- Upload multiple reference images (1-4)
- Write detailed prompts describing desired output
- Real-time image preview and validation
- Direct download of generated images
- Modern, responsive web interface

### 🎭 **AI Image Masking**

Launch the image masking interface:
```bash
# Easy launcher
python mask_runner.py

# Or direct Streamlit
streamlit run image_masking_streamlit.py
```

**Features:**
- Upload base image and mask image separately
- Generate new content in masked areas only
- Choose between standard and high quality output
- Custom output filename specification
- Clear mask guidelines and instructions

### 💻 **DALL-E Image Editor (Command Line)**

Run the command-line image editor:
```bash
python OpenAI.py
```

**Features:**
- Edit existing PNG images with text prompts
- Interactive command-line interface
- Robust error handling and validation

### 🔑 **API Key Setup**

#### Method 1: Environment Variable (Recommended)
```bash
# Windows
set OPENAI_API_KEY=your_api_key_here

# Linux/Mac
export OPENAI_API_KEY=your_api_key_here
```

#### Method 2: Direct Input
Enter your API key directly in the web interface or when prompted by the CLI.

## Example Usage

### GPT-4 Vision Generator
1. **Upload Images**: Drag and drop 1-4 reference images
2. **Write Prompt**: Describe what you want to generate
   ```
   "Create a futuristic cityscape combining the architectural styles 
   from the uploaded images, with neon lights and flying cars"
   ```
3. **Generate**: Click "Generate Image" and wait for results
4. **Download**: Save your generated images

### AI Image Masking
1. **Upload Base Image**: Upload the image you want to edit
2. **Upload Mask Image**: Upload a mask (white = generate new content, black = keep original)
3. **Write Prompt**: Describe what to generate in the masked area
   ```
   "A beautiful sunset sky with orange and pink clouds"
   ```
4. **Generate**: Click "Generate Masked Image" and wait for results
5. **Download**: Save your masked image with custom filename

### DALL-E Editor
```
=== OpenAI Image Editing Tool ===

Enter the path to your base PNG image (<4MB): C:\images\my_photo.png
Enter a prompt describing the desired change: Add a sunset background
Enter your OpenAI API key (or press Enter to use OPENAI_API_KEY env variable): 

Sending request to OpenAI API...
Downloading generated image...
Generated image saved as: generated_image.png

=== Success! ===
Your edited image has been saved as: generated_image.png
```

## File Structure

```
├── streamlit_app.py              # GPT-4 Vision web application
├── image_masking_streamlit.py    # AI Image Masking web application
├── OpenAI.py                     # DALL-E command-line editor
├── Image_gen_scratch.py          # Original GPT-4 Vision code
├── image_mask.py                 # Original image masking code
├── run_image_generator.py        # Launcher for GPT-4 Vision app
├── mask_runner.py                # Launcher for image masking app
├── requirements.txt              # Python dependencies
├── README.md                     # This documentation
└── .streamlit/
    └── config.toml              # Streamlit configuration
```

## Error Handling

Both applications include comprehensive error handling:

- **Invalid file paths**: Clear error messages and retry prompts
- **Wrong file formats**: Format validation with helpful suggestions
- **File size limits**: Automatic size checking
- **Invalid API keys**: Authentication error messages
- **Rate limiting**: User-friendly retry suggestions
- **Network issues**: Graceful handling of connection problems

## Output

### GPT-4 Vision Generator
- Generated images displayed directly in browser
- Download buttons for each generated image
- Real-time progress indicators and status messages

### AI Image Masking
- Generated masked images displayed directly in browser
- Download buttons with custom filenames
- Images also saved locally with specified filename
- Real-time progress indicators and status messages

### DALL-E Editor
- Generated images saved as `generated_image.png` in current directory
- Console output with API URLs and file paths
- Clear success/error messages

## Troubleshooting

**"File not found"**: Ensure the file path is correct and the file exists
**"Invalid file format"**: Use supported formats (PNG for DALL-E, multiple formats for GPT-4)
**"File too large"**: Compress or resize your images
**"Invalid API key"**: Check your OpenAI API key and ensure you have the required API access
**"Rate limit exceeded"**: Wait a moment and try again
**"No images generated"**: Check your prompt and ensure it's descriptive enough

## API Requirements

- **DALL-E Editor**: Requires DALL-E API access
- **GPT-4 Vision Generator**: Requires GPT-4 Vision API access with image generation tools
- Both require sufficient API credits in your OpenAI account

## Notes

- GPT-4 Vision generator supports multiple image formats and larger file sizes
- DALL-E editor is optimized for PNG images under 4MB
- Both applications use the latest OpenAI API versions
- For more information, see the [OpenAI API documentation](https://platform.openai.com/docs/)

---

*Made by Anant with ❤️* 