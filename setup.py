#!/usr/bin/env python3
"""
Setup script for CVAT download tool
"""

import subprocess
import sys
import os
import shutil

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install requirements: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            print("Creating .env file from env.example...")
            shutil.copy('env.example', '.env')
            print("✓ .env file created from env.example")
        else:
            print("Creating .env file...")
            env_content = """# CVAT Download Configuration
# Modify these values as needed

# CVAT Credentials
CVAT_EMAIL=jeffhong824@gmail.com
CVAT_PASSWORD=Jeff840606

# Process Configuration
PROCESS_TYPE=yolo
# PROCESS_TYPE=cvat_for_video

# Directory Configuration
TARGET_DIR=dataset/{process_type}_type/project
ANNOTATION_FILE_PATH=annotation/標註工作分配_20251022.xlsx
DOWNLOAD_DIR=./downloads

# Processing Options
SAVE_IMG=False
HEADLESS=False
TIMEOUT=120

# Sheets to process
SHEETS_TO_PROCESS=DA1,DA2,DA3,DA4_新竹,DA5,DA6,DA7_新竹,內視鏡1,內視鏡2,內視鏡3,內視鏡4,內視鏡5
"""
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(env_content)
            print("✓ .env file created")
    else:
        print("✓ .env file already exists")

def check_directories():
    """Check and create necessary directories"""
    directories = [
        'annotation',
        'dataset/yolo_type/project',
        'dataset/cvat_for_video_type/project',
        'downloads'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory exists: {directory}")
    
    # Also check if config.py exists and create directories based on TARGET_DIR
    try:
        from config import TARGET_DIR
        if not os.path.exists(TARGET_DIR):
            os.makedirs(TARGET_DIR, exist_ok=True)
            print(f"✓ Created target directory: {TARGET_DIR}")
        else:
            print(f"✓ Target directory exists: {TARGET_DIR}")
    except ImportError:
        print("⚠ config.py not found, skipping dynamic target directory check")

def main():
    """Main setup function"""
    print("CVAT Download Tool Setup")
    print("=" * 30)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please install requirements manually.")
        return
    
    # Create .env file
    create_env_file()
    
    # Check directories
    check_directories()
    
    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your CVAT credentials")
    print("2. Place your annotation Excel file in the annotation/ directory")
    print("3. Run: python download_cvat.py")

if __name__ == "__main__":
    main()
