#!/usr/bin/env python3
"""
Launcher script for the AI Image Masking Streamlit app.
Uses GPT-4 Vision with image masking capabilities.
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['streamlit', 'openai', 'requests', 'PIL']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install dependencies with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main launcher function."""
    print("🎭 AI Image Masking - GPT-4 Vision")
    print("=" * 50)
    print("Generate new content in masked areas of your images")
    print("using GPT-4 Vision with image masking capabilities")
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies found!")
    print("🚀 Starting Streamlit app...")
    print("📱 The app will open in your default browser")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "image_masking_streamlit.py",
            "--server.port", "8502",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 