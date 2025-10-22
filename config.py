"""
Configuration file for CVAT download script
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# CVAT Credentials
CVAT_EMAIL = os.getenv('CVAT_EMAIL', 'jeffhong824@gmail.com')
CVAT_PASSWORD = os.getenv('CVAT_PASSWORD', 'Jeff840606')

# Process Configuration
PROCESS_TYPE = os.getenv('PROCESS_TYPE', 'yolo')
# PROCESS_TYPE = 'cvat_for_video'

# Directory Configuration
TARGET_DIR = os.getenv('TARGET_DIR')
if TARGET_DIR is None:
    TARGET_DIR = f'dataset/{PROCESS_TYPE}_type/project'
ANNOTATION_FILE_PATH = os.getenv('ANNOTATION_FILE_PATH', 'annotation/標註工作分配_20251022.xlsx')
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', os.path.join(os.getcwd(), 'downloads'))

# Processing Options
SAVE_IMG = os.getenv('SAVE_IMG', 'False').lower() == 'true'
HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
TIMEOUT = int(os.getenv('TIMEOUT', '120'))

# Sheets to process
SHEETS_TO_PROCESS = os.getenv('SHEETS_TO_PROCESS', 
    'DA1').split(',')
    # 'DA1,DA2,DA3,DA4_新竹,DA5,DA6,DA7_新竹,內視鏡1,內視鏡2,內視鏡3,內視鏡4,內視鏡5').split(',')

# CVAT URLs
CVAT_LOGIN_URL = 'https://aiailab.synology.me/projects'
