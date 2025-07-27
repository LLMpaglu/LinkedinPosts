import streamlit as st
import os
import json
import requests
from openai import OpenAI
import base64
import tempfile
from pathlib import Path
import io
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI()

def create_file(file_path):
    """Create a file in OpenAI for vision processing."""
    client = get_openai_client()
    with open(file_path, "rb") as file_content:
        result = client.files.create(
            file=file_content,
            purpose="vision",
        )
        return result.id

def encode_image(file_path):
    """Encode image to base64."""
    with open(file_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode("utf-8")
    return base64_image

def validate_image_file(uploaded_file):
    """Validate uploaded image file."""
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file size (max 20MB for OpenAI)
    if uploaded_file.size > 20 * 1024 * 1024:
        return False, "File size must be less than 20MB"
    
    # Check file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    if uploaded_file.type not in allowed_types:
        return False, f"File type {uploaded_file.type} not supported. Use: {', '.join(allowed_types)}"
    
    return True, "File is valid"

def save_uploaded_file(uploaded_file):
    """Save uploaded file to temporary location."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

def main():
    st.title("🎨 AI Image Generator")
    st.markdown("Generate new images using GPT-4 Vision and multiple input images")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key or set OPENAI_API_KEY environment variable"
        )
        
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            st.error("⚠️ OpenAI API key is required!")
            st.info("Please enter your API key in the sidebar or set the OPENAI_API_KEY environment variable.")
            return
        
        # Set API key for client
        os.environ["OPENAI_API_KEY"] = api_key
        
        st.markdown("---")
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. Upload 1-4 reference images
        2. Enter a detailed prompt describing what you want to generate
        3. Click 'Generate Image' to create your new image
        """)
        
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Use clear, descriptive prompts
        - Upload high-quality reference images
        - Be specific about style, composition, and details
        - Multiple images help the AI understand your vision better
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Reference Images")
        st.markdown("Upload 1-4 images to guide the AI generation")
        
        # File uploader for multiple images
        uploaded_files = st.file_uploader(
            "Choose image files",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            accept_multiple_files=True,
            help="Upload 1-4 images (max 20MB each)"
        )
        
        # Validate uploaded files
        valid_files = []
        if uploaded_files:
            for i, uploaded_file in enumerate(uploaded_files):
                is_valid, message = validate_image_file(uploaded_file)
                if is_valid:
                    valid_files.append(uploaded_file)
                    st.success(f"✅ {uploaded_file.name} - {message}")
                else:
                    st.error(f"❌ {uploaded_file.name} - {message}")
            
            if not valid_files:
                st.error("No valid images uploaded. Please upload at least one valid image.")
                return
            
            # Display uploaded images
            st.subheader("📷 Uploaded Images")
            cols = st.columns(min(len(valid_files), 3))
            for i, uploaded_file in enumerate(valid_files):
                with cols[i % 3]:
                    st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)
    
    with col2:
        st.header("✍️ Generation Prompt")
        
        # Prompt input
        prompt = st.text_area(
            "Describe what you want to generate",
            placeholder="e.g., Create a futuristic cityscape combining the architectural styles from the uploaded images, with neon lights and flying cars...",
            height=200,
            max_chars=4000,
            help="Be detailed and specific about what you want to generate"
        )
        
        # Show character count
        if prompt:
            st.caption(f"Characters: {len(prompt)}/4000")
        
        # Generate button
        if st.button("🚀 Generate Image", type="primary", disabled=not (valid_files and prompt)):
            if not valid_files:
                st.error("Please upload at least one valid image!")
                return
            if not prompt:
                st.error("Please enter a prompt!")
                return
            
            try:
                with st.spinner("🔄 Processing your request..."):
                    # Save uploaded files temporarily
                    temp_files = []
                    base64_images = []
                    file_ids = []
                    
                    try:
                        # Process each uploaded file
                        for uploaded_file in valid_files:
                            temp_path = save_uploaded_file(uploaded_file)
                            temp_files.append(temp_path)
                            
                            # Create base64 encoding
                            base64_image = encode_image(temp_path)
                            base64_images.append(base64_image)
                            
                            # Create file ID for OpenAI
                            file_id = create_file(temp_path)
                            file_ids.append(file_id)
                        
                        # Prepare content for API call
                        content = [{"type": "input_text", "text": prompt}]
                        
                        # Add images to content
                        for base64_image in base64_images:
                            content.append({
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{base64_image}",
                            })
                        
                        for file_id in file_ids:
                            content.append({
                                "type": "input_image",
                                "file_id": file_id,
                            })
                        
                        # Make API call
                        client = get_openai_client()
                        response = client.responses.create(
                            model="gpt-4o",
                            input=[
                                {
                                    "role": "user",
                                    "content": content,
                                }
                            ],
                            tools=[{"type": "image_generation"}],
                        )
                        
                        # Extract image generation results
                        image_generation_calls = [
                            output
                            for output in response.output
                            if output.type == "image_generation_call"
                        ]
                        
                        image_data = [output.result for output in image_generation_calls]
                        
                        if image_data:
                            st.success("✅ Image generated successfully!")
                            
                            # Display and save generated images
                            st.subheader("🎨 Generated Images")
                            
                            for i, image_base64 in enumerate(image_data):
                                # Decode and display image
                                image_bytes = base64.b64decode(image_base64)
                                
                                # Display image
                                st.image(image_bytes, caption=f"Generated Image {i+1}", use_column_width=True)
                                
                                # Download button
                                st.download_button(
                                    label=f"📥 Download Image {i+1}",
                                    data=image_bytes,
                                    file_name=f"generated_image_{i+1}.png",
                                    mime="image/png"
                                )
                        else:
                            st.error("❌ No images were generated")
                            if hasattr(response.output, 'content'):
                                st.text("API Response:")
                                st.text(response.output.content)
                    
                    finally:
                        # Clean up temporary files
                        for temp_file in temp_files:
                            try:
                                os.unlink(temp_file)
                            except:
                                pass
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Made by Anant with ❤️</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 