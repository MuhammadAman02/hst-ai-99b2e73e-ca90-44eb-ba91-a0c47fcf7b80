"""
Nike Shoe Store - Main Application Entry Point
Production-ready e-commerce application with modern UI
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_dependencies():
    """Verify all required dependencies are available."""
    required_packages = ['nicegui', 'uvicorn', 'python_dotenv', 'httpx']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print(f"📦 Install with: pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies available")
    return True

if __name__ == "__main__":
    if check_dependencies():
        # Import and start the application
        from app.main import start_app
        start_app()
    else:
        exit(1)