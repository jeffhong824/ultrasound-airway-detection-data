# Ultrasound Airway Detection Data

This repository contains tools for downloading and managing ultrasound airway detection datasets from CVAT (Computer Vision Annotation Tool).

## Features

- Automated dataset download from CVAT platform
- Excel-based annotation status tracking
- Support for both YOLO and CVAT video formats
- Configurable download settings
- Progress tracking and error handling

## Requirements

- **Python**: 3.8 or higher
- **Chrome Browser**: Required for Selenium WebDriver
- **ChromeDriver**: Automatically managed by webdriver-manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ultrasound-airway-detection-data
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Chrome browser if not already installed.

## Configuration

### Method 1: Environment Variables (.env file)

Copy `env.example` to `.env` and modify the values:

```env
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
```

### Method 2: Direct Configuration (config.py)

Edit the `config.py` file directly to modify settings.

## Usage

### Prerequisites

1. **Annotation File**: Place your annotation Excel file in the `annotation/` directory
2. **Target Directory**: Ensure the target directory exists or the script will create it
3. **CVAT Access**: Ensure you have valid CVAT credentials

### Running the Script

```bash
python download_cvat.py
```

### Process Flow

1. **Annotation Processing**: The script reads the Excel file and identifies items marked as ready for download (containing "V" or "v" in the completion status)
2. **Existing Files Check**: Checks for already downloaded files to avoid duplicates
3. **Download List Generation**: Creates a filtered list of items to download
4. **Automated Download**: Uses Selenium to automate the CVAT download process
5. **File Management**: Automatically moves downloaded files to the target directory
6. **Report Generation**: Creates a detailed TXT report with download statistics and file lists

### Configuration Options

- `PROCESS_TYPE`: Choose between "yolo" or "cvat_for_video" format
- `SAVE_IMG`: Whether to save images during export
- `HEADLESS`: Run Chrome in headless mode (no GUI)
- `TIMEOUT`: Maximum wait time for downloads (seconds)
- `SHEETS_TO_PROCESS`: Excel sheets to process for annotations

### Download Report

After each download session, the script generates a detailed TXT report containing:

- **Excel Statistics**: Number of items marked as ready for download
- **Existing Files**: Number of files already in the target directory
- **Download Statistics**: Success/failure counts and success rate
- **Success List**: Complete list of successfully downloaded files
- **Failure List**: List of files that failed to download
- **Detailed Summary**: Comprehensive statistics breakdown

The report file is saved as `download_report_YYYYMMDD_HHMMSS.txt` in the dataset directory.

### Git Ignore

The `.gitignore` file is configured to ignore:
- `*.zip` files (downloaded datasets)
- `*.txt` files (download reports)
- `.env` files (environment variables with credentials)
- Python cache files and virtual environments
- IDE and OS temporary files

This ensures that large dataset files and sensitive configuration files are not committed to the repository.

## File Structure

```
ultrasound-airway-detection-data/
├── annotation/                    # Annotation Excel files
├── dataset/                       # Downloaded datasets
│   ├── yolo_type/project/        # YOLO format datasets
│   └── cvat_for_video_type/project/  # CVAT video format datasets
├── download/                      # Original Jupyter notebook
│   └── download_cvat.ipynb       # Original Jupyter notebook
├── downloads/                     # Temporary download directory
├── config.py                      # Configuration file
├── download_cvat.py              # Main Python script
├── setup.py                       # Setup script
├── requirements.txt               # Python dependencies
├── env.example                    # Environment variables template
├── .gitignore                     # Git ignore file
└── README.md                     # This file
```

## Troubleshooting

### Common Issues

1. **ChromeDriver Issues**: The script uses webdriver-manager to automatically handle ChromeDriver installation
2. **Login Failures**: Verify CVAT credentials and network connectivity
3. **Download Timeouts**: Increase the `TIMEOUT` value for slower connections
4. **File Permission Errors**: Ensure write permissions for target directories
5. **Virus Scan Failures**: Some downloads may fail virus scanning due to false positives

### Virus Scan Issues

If downloads show "病毒掃描失敗" (Virus scan failed), this is usually a false positive. Solutions:

1. **Use Local Downloads Directory**: The script now uses `./downloads` instead of system Downloads folder
2. **Add Exception**: Add the project directory to your antivirus exception list
3. **Temporarily Disable**: Temporarily disable real-time protection during downloads
4. **Manual Verification**: Manually scan the files if needed

### Debug Mode

Run with `HEADLESS=False` to see the browser automation in action:

```env
HEADLESS=False
```

## Dependencies

- `pandas`: Excel file processing
- `selenium`: Web automation
- `tqdm`: Progress bars
- `python-dotenv`: Environment variable management
- `openpyxl`: Excel file support
- `webdriver-manager`: ChromeDriver management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]