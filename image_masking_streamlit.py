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
    page_title="AI Image Masking",
    page_icon="🎭",
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
    st.title("🎭 AI Image Masking")
    st.markdown("Generate new content in masked areas of your images using GPT-4 Vision")
    
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
        
        # Quality selection
        quality = st.selectbox(
            "Image Quality",
            ["standard", "high"],
            index=1,
            help="Higher quality takes longer but produces better results"
        )
        
        st.markdown("---")
        st.markdown("### 📋 Instructions")
        st.markdown("""
        1. Upload a base image (the image you want to edit)
        2. Upload a mask image (white areas = where to generate new content)
        3. Enter a prompt describing what to generate in the masked area
        4. Click 'Generate' to create your masked image
        """)
        
        st.markdown("### 🎨 Mask Guidelines")
        st.markdown("""
        - **White areas** in mask = where new content will be generated
        - **Black areas** in mask = where original image is preserved
        - **Gray areas** = partial blending between old and new
        - Use precise masks for best results
        """)
        
        st.markdown("### 💡 Tips")
        st.markdown("""
        - Be specific about what you want in the masked area
        - Ensure mask and base image have the same dimensions
        - High quality setting produces better results but costs more
        - Use clear, descriptive prompts for best results
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Images")
        
        # Base image upload
        st.subheader("🖼️ Base Image")
        base_image = st.file_uploader(
            "Choose your base image",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            help="Upload the image you want to edit (max 20MB)"
        )
        
        if base_image is not None:
            # Validate base image
            is_valid, message = validate_image_file(base_image)
            if is_valid:
                st.success(f"✅ Base image: {message}")
                st.image(base_image, caption="Base Image", use_column_width=True)
            else:
                st.error(f"❌ Base image: {message}")
                return
        
        # Mask image upload
        st.subheader("🎭 Mask Image")
        mask_image = st.file_uploader(
            "Choose your mask image",
            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
            help="Upload the mask image (white = generate new content, black = keep original)"
        )
        
        if mask_image is not None:
            # Validate mask image
            is_valid, message = validate_image_file(mask_image)
            if is_valid:
                st.success(f"✅ Mask image: {message}")
                st.image(mask_image, caption="Mask Image", use_column_width=True)
            else:
                st.error(f"❌ Mask image: {message}")
                return
    
    with col2:
        st.header("✍️ Generation Prompt")
        
        # Prompt input
        prompt = st.text_area(
            "Describe what you want to generate in the masked area",
            placeholder="e.g., A beautiful sunset sky, A modern furniture piece, A lush garden with flowers...",
            height=200,
            max_chars=4000,
            help="Be specific about what you want to generate in the white areas of your mask"
        )
        
        # Show character count
        if prompt:
            st.caption(f"Characters: {len(prompt)}/4000")
        
        # Output filename
        output_filename = st.text_input(
            "Output filename",
            value="masked_image.png",
            help="Name for the generated image file"
        )
        
        # Generate button
        if st.button("🚀 Generate Masked Image", type="primary", disabled=not (base_image and mask_image and prompt)):
            if not base_image:
                st.error("Please upload a base image!")
                return
            if not mask_image:
                st.error("Please upload a mask image!")
                return
            if not prompt:
                st.error("Please enter a prompt!")
                return
            
            try:
                with st.spinner("🔄 Processing your masked image..."):
                    # Save uploaded files temporarily
                    temp_files = []
                    
                    try:
                        # Save base image
                        base_path = save_uploaded_file(base_image)
                        temp_files.append(base_path)
                        
                        # Save mask image
                        mask_path = save_uploaded_file(mask_image)
                        temp_files.append(mask_path)
                        
                        # Create file IDs for OpenAI
                        base_file_id = create_file(base_path)
                        mask_file_id = create_file(mask_path)
                        
                        # Make API call
                        client = get_openai_client()
                        response = client.responses.create(
                            model="gpt-4o",
                            input=[
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "input_text",
                                            "text": prompt,
                                        },
                                        {
                                            "type": "input_image",
                                            "file_id": base_file_id,
                                        }
                                    ],
                                },
                            ],
                            tools=[
                                {
                                    "type": "image_generation",
                                    "quality": quality,
                                    "input_image_mask": {
                                        "file_id": mask_file_id,
                                    },
                                },
                            ],
                        )
                        
                        # Extract image generation results
                        image_data = [
                            output.result
                            for output in response.output
                            if output.type == "image_generation_call"
                        ]
                        
                        if image_data:
                            st.success("✅ Masked image generated successfully!")
                            
                            # Display and save generated image
                            st.subheader("🎨 Generated Masked Image")
                            
                            image_base64 = image_data[0]
                            image_bytes = base64.b64decode(image_base64)
                            
                            # Display image
                            st.image(image_bytes, caption="Generated Masked Image", use_column_width=True)
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Masked Image",
                                data=image_bytes,
                                file_name=output_filename,
                                mime="image/png"
                            )
                            
                            # Save to file
                            with open(output_filename, "wb") as f:
                                f.write(image_bytes)
                            st.info(f"💾 Image also saved as: {output_filename}")
                            
                        else:
                            st.error("❌ No image was generated")
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