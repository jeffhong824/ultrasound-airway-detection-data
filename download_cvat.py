#!/usr/bin/env python3
"""
CVAT Dataset Download Script

This script downloads datasets from CVAT based on annotation status from Excel files.
It processes annotation files, identifies ready-to-download items, and automatically
downloads them using Selenium WebDriver.

Usage:
    python download_cvat.py

Configuration:
    Edit config.py or create .env file to modify settings
"""

import os
import time
import shutil
from datetime import datetime
from time import sleep
from tqdm import tqdm
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from config import *


def process_annotation_file():
    """
    Process annotation Excel file and identify ready-to-download items
    """
    print("Processing annotation file...")
    
    # Initialize lists
    ready_to_download = []
    not_ready_to_download = []
    
    # Process each specified sheet
    for sheet in SHEETS_TO_PROCESS:
        count_ready = 0
        count_not_ready = 0
        count_annotation_error = 0
        
        try:
            df = pd.read_excel(ANNOTATION_FILE_PATH, sheet_name=sheet, dtype={"cl_grade": str})
        except Exception as e:
            print(f"Error reading sheet {sheet}: {e}")
            continue
            
        # Get first column name (ID column)
        id_column = df.columns[0]
        
        for _, row in df.iterrows():
            id_value = row[id_column]
            annotation = str(row.get("完成", ""))
            cl_grade = str(row.get("cl_grade", "")).strip()
            
            # Format ID value - handle .0 suffix from pandas
            id_str = str(id_value)
            if id_str.endswith('.0'):
                id_str = id_str[:-2]  # Remove .0 suffix
            
            if id_str.isdigit() and len(id_str) == 6:
                id_value_re = "0" + str(int(id_str))
            elif id_str.isdigit() and len(id_str) == 7:
                id_value_re = str(int(id_str))
            else:
                id_value_re = id_str
            
            # Add prefix based on sheet type
            if sheet.find("DA") != -1:
                id_value_re = "DA" + id_value_re
            elif sheet.find("內視鏡") != -1:
                id_value_re = "ES" + id_value_re
            
            # Check if ready for download - exactly like notebook
            if (annotation.find("V") != -1 or annotation.find("v") != -1):
                ready_to_download.append(id_value_re)
                count_ready += 1
            elif (str(annotation) != "nan" and annotation.find("V") == -1 and annotation.find("v") == -1):
                not_ready_to_download.append(id_value_re)
                count_annotation_error += 1
            else:
                not_ready_to_download.append(id_value_re)
                count_not_ready += 1
        
        print(sheet, "count_ready", count_ready, "count_annotation_error", count_annotation_error, "count_not_ready", count_not_ready)
    
    print("準備下載名單:", len(ready_to_download), ready_to_download)
    print("尚未準備下載名單:", len(not_ready_to_download), not_ready_to_download)
    
    return ready_to_download, not_ready_to_download


def ensure_target_directory():
    """
    Ensure target directory exists, create if not
    """
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR, exist_ok=True)
        print(f"Created directory: {TARGET_DIR}")
    else:
        print(f"Target directory exists: {TARGET_DIR}")


def get_existing_files():
    """
    Get list of already downloaded files
    """
    print("Checking existing files...")
    
    # Ensure target directory exists
    ensure_target_directory()
    
    da_items = []
    try:
        for item in os.listdir(TARGET_DIR):
            if item.endswith('.zip'):
                da_items.append(str(item).replace(".zip", ""))
    except FileNotFoundError:
        print(f"Directory {TARGET_DIR} not found, will be created when needed")
        return []
    
    print(f"整理後的名單: {len(da_items)} items")
    return da_items


def get_download_list(ready_to_download, existing_files):
    """
    Get filtered list of items to download
    """
    # Remove duplicates and already downloaded items
    filtered_list = [item for item in ready_to_download if item not in set(existing_files)]
    
    print(f"要下載的名單: {len(filtered_list)} items")
    
    return filtered_list


def setup_chrome_driver():
    """
    Setup Chrome WebDriver with options
    """
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument('--headless')
    
    # Set download directory
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.path.abspath(DOWNLOAD_DIR),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    
    driver = Chrome(options=chrome_options)
    return driver


def download_single_dataset(driver, patient_ID):
    """
    Download dataset for a single patient ID - following exact notebook logic
    """
    print(f"Processing {patient_ID}...")
    
    ## login - exactly like notebook
    driver.get(CVAT_LOGIN_URL)
    
    # Wait for page to load completely
    sleep(3)  # Wait 3 seconds for page to load
    
    try_login = True
    stop_time = 10
    stop_time_count = 0
    while try_login:
        try:
            driver.find_element(By.XPATH, '//*[@id="credential"]').send_keys(CVAT_EMAIL)
            try_login = False
        except:
            try_login = True
            stop_time_count += 1
            if stop_time_count >= stop_time:
                try_login = False
    if stop_time_count < stop_time:
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(CVAT_PASSWORD)
        driver.find_element(By.XPATH, '//*[@id="root"]/section/section/main/div/div[2]/div/div/div/form/div[3]/div/div/div/button').click()
        
        # Wait for login to complete
        sleep(2)

    ## find patient ID - exactly like notebook
    try_search = True
    while try_search:
        try:
            driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div[1]/div/div[1]/span/span/input').send_keys(patient_ID)
            try_search = False
        except:
            try_search = True

    try_click = True
    while try_click:
        try:
            driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div[1]/div/div[1]/span/span/span/button').click()
            try_click = False
        except:
            try_click = True
    
    # Wait for search results to load
    sleep(2)

    ## Export dataset - exactly like notebook
    try_point_button = True
    while try_point_button:
        try:
            driver.find_element(By.XPATH, '//*[@id="root"]/section/main/div/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div/div[2]/button').click()
            try_point_button = False
        except:
            try_point_button = True

    try_export_button = True
    while try_export_button:
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div/div/ul/li[1]/span').click()
            try_export_button = False
        except:
            try_export_button = True
    
    # Wait for export menu to load
    sleep(1)
    
    try_export_dataset_button = True
    while try_export_dataset_button:
        try:
            driver.find_element(By.XPATH, '//*[@id="Export dataset"]/div[1]/div[2]/div/div/div').click()
            try_export_dataset_button = False
        except:
            try_export_dataset_button = True
    
    # Wait for export dialog to load
    sleep(1)

    ## Select format - exactly like notebook
    try_select_button = True
    while try_select_button:
        try:
            if PROCESS_TYPE[:4] == "yolo":
                driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[24]').click()
            elif PROCESS_TYPE == "cvat_for_video":
                driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div/div/div/div[6]/div').click()
            try_select_button = False
        except:
            try_select_button = True

    ## save images - exactly like notebook
    if SAVE_IMG == True:
        driver.find_element(By.XPATH, '//*[@id="Export dataset_saveImages"]').click()

    ## dataset name - exactly like notebook
    driver.find_element(By.XPATH, '//*[@id="Export dataset_customName"]').send_keys(patient_ID)

    ## OK - exactly like notebook
    driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div/div[2]/div[3]/button[2]').click()
    
    return True


def wait_for_download(patient_ID):
    """
    Wait for download to complete and move file to target directory
    """
    expected_filename = f"{patient_ID}.zip"
    downloaded = False
    start_time = time.time()
    
    print(f"Waiting for download: {expected_filename}")
    
    # Ensure target directory exists before moving files
    ensure_target_directory()
    
    while not downloaded and time.time() - start_time < TIMEOUT:
        try:
            for filename in os.listdir(DOWNLOAD_DIR):
                if filename.endswith(".zip") and expected_filename in filename:
                    source_path = os.path.join(DOWNLOAD_DIR, filename)
                    dest_path = os.path.join(TARGET_DIR, filename)
                    
                    # Move file
                    shutil.move(source_path, dest_path)
                    print(f"Downloaded and moved: {filename}")
                    downloaded = True
                    break
        except Exception as e:
            print(f"Error checking downloads: {e}")
        
        if not downloaded:
            time.sleep(2)  # Check every 2 seconds
    
    if not downloaded:
        print(f"[警告] 等待 {TIMEOUT} 秒後仍未找到檔案 {expected_filename}，跳過此 ID。")
        return False
    
    return True


def generate_download_report(ready_to_download, existing_files, download_list, successful_downloads, failed_downloads, failed_items):
    """
    Generate a detailed download report
    """
    report_filename = f"download_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_path = os.path.join(os.path.dirname(TARGET_DIR), report_filename)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("CVAT Dataset Download Report\n")
        f.write("=" * 50 + "\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Process Type: {PROCESS_TYPE}\n")
        f.write(f"Target Directory: {TARGET_DIR}\n")
        f.write(f"Annotation File: {ANNOTATION_FILE_PATH}\n\n")
        
        # Excel 統計
        f.write("Excel 檔案統計:\n")
        f.write("-" * 30 + "\n")
        f.write(f"從 Excel 預估要下載的數量: {len(ready_to_download)}\n")
        f.write(f"已存在的檔案數量: {len(existing_files)}\n")
        f.write(f"實際需要下載的數量: {len(download_list)}\n\n")
        
        # 下載結果統計
        f.write("下載結果統計:\n")
        f.write("-" * 30 + "\n")
        f.write(f"成功下載: {successful_downloads}\n")
        f.write(f"下載失敗: {failed_downloads}\n")
        f.write(f"成功率: {(successful_downloads / len(download_list) * 100):.1f}%\n\n")
        
        # 成功下載的檔案列表
        f.write("成功下載的檔案:\n")
        f.write("-" * 30 + "\n")
        success_files = []
        for item in os.listdir(TARGET_DIR):
            if item.endswith('.zip'):
                success_files.append(item.replace('.zip', ''))
        
        success_files.sort()
        for i, file in enumerate(success_files, 1):
            f.write(f"{i:3d}. {file}\n")
        
        f.write(f"\n總計成功檔案數: {len(success_files)}\n\n")
        
        # 失敗的檔案列表
        if failed_items:
            f.write("下載失敗的檔案:\n")
            f.write("-" * 30 + "\n")
            for i, item in enumerate(failed_items, 1):
                f.write(f"{i:3d}. {item}\n")
            f.write(f"\n總計失敗檔案數: {len(failed_items)}\n\n")
        
        # 詳細統計
        f.write("詳細統計:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Excel 中標記為完成 (V/v): {len(ready_to_download)}\n")
        f.write(f"資料夾中已存在: {len(existing_files)}\n")
        f.write(f"需要下載: {len(download_list)}\n")
        f.write(f"實際成功: {successful_downloads}\n")
        f.write(f"實際失敗: {failed_downloads}\n")
        f.write(f"剩餘未下載: {len(download_list) - successful_downloads - failed_downloads}\n")
    
    print(f"\n下載報告已生成: {report_path}")
    return report_path


def main():
    """
    Main function to orchestrate the download process
    """
    print("CVAT Dataset Download Script")
    print("=" * 50)
    
    # Process annotation file
    ready_to_download, not_ready_to_download = process_annotation_file()
    
    # Get existing files
    existing_files = get_existing_files()
    
    # Get download list
    download_list = get_download_list(ready_to_download, existing_files)
    
    if not download_list:
        print("No items to download. Exiting.")
        return
    
    # Setup Chrome driver
    driver = setup_chrome_driver()
    
    try:
        # Download datasets
        successful_downloads = 0
        failed_downloads = 0
        failed_items = []
        
        for patient_ID in tqdm(download_list, desc="Downloading datasets"):
            try:
                # Download single dataset (following exact notebook logic)
                if download_single_dataset(driver, patient_ID):
                    if wait_for_download(patient_ID):
                        successful_downloads += 1
                    else:
                        failed_downloads += 1
                        failed_items.append(patient_ID)
                else:
                    failed_downloads += 1
                    failed_items.append(patient_ID)
            except Exception as e:
                print(f"Error processing {patient_ID}: {e}")
                failed_downloads += 1
                failed_items.append(patient_ID)
        
        print(f"\nDownload Summary:")
        print(f"Successful: {successful_downloads}")
        print(f"Failed: {failed_downloads}")
        
        # Generate detailed report
        report_path = generate_download_report(
            ready_to_download, existing_files, download_list, 
            successful_downloads, failed_downloads, failed_items
        )
        
    finally:
        driver.quit()
        print("Browser closed.")


if __name__ == "__main__":
    main()
