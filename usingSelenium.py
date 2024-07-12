from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import pandas as pd


edge_options = webdriver.EdgeOptions()
edge_options.add_argument("user-data-dir=C:\\Program Files (x86)\\Microsoft\\Edge\\Application")
#ser = Service("C:\\edge\\edgedriver_win64\\msedgedriver.exe")
ser = Service("C:\\Users\\yanqinchen\\AppData\\Local\\Temp\\this\\MicrosoftWebDriver.exe")

driver = webdriver.Edge(options = edge_options, service=ser)

# Open the login page
driver.get("https://meta.files.com/login")

wait = WebDriverWait(driver, 20)
try:
    username_field = wait.until(EC.presence_of_element_located((By.ID, "form-username")))
    password_field = wait.until(EC.presence_of_element_located((By.ID, "form-password")))

except Exception as e:
    print("An error occurred while finding the elements: ", e)
    driver.quit()
    exit()

username_field.send_keys("XXX")
password_field.send_keys("XXX")
password_field.send_keys(Keys.RETURN)

driver.get("https://meta.files.com/files/Jetcost/Partners_report/CTRIP/Clicks")

try:
    while True:
        #click to select all files in one page
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "Checkbox")))
        driver.find_element(By.CLASS_NAME, "Checkbox").click()
        #go to next page
        y=500
        while len(driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Next page']")) == 0:
            driver.execute_script("window.scrollTo(0, " +str(y) +")")
            y+=500
        
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.PaginationNavNext"))
        )

        # Check if the "Next page" button is disabled
        if next_button.get_attribute("aria-disabled") == "true":
            print("Reached the last page.")
            break

        # Click the "Next page" button
        next_button.click()

except:
    print("Something is wrong.")

#download files
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "buttonLabel"))) 
driver.find_element(By.CLASS_NAME, "buttonLabel").click()

def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

#unzip the files and restore it in extracted_folder
import os
import zipfile

# Path to the ZIP file
zip_file_path = r"C:\Users\yanqinchen\Downloads\Files.zip"
# Directory where the ZIP file will be extracted
extracted_folder = r"C:\Users\yanqinchen\Desktop\clicksfile"

# Ensure the extracted files folder exists
os.makedirs(extracted_folder, exist_ok=True)

# Clear the extracted files folder
clear_folder(extracted_folder)

# Unzip the specified file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)
    print(f"Extracted {zip_file_path} to {extracted_folder}")

# Optionally delete the zip file after extraction
os.remove(zip_file_path)
print(f"Deleted {zip_file_path}")

def  get_clicks_day(df):
    df1=df.iloc[:,[1,4,5,6]]
    df1.insert(0, 'date', df.columns[6])
    df1.columns=['date','country','from','to','clicks']
    return df1

column_names=['date','country','from','to','clicks']
result=pd.DataFrame(columns=column_names)
for root, dirs, files in os.walk(extracted_folder):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            df = pd.read_csv(file_path)
            df1=get_clicks_day(df)
        result=pd.concat([result,df1],axis=0,ignore_index=True)

result.to_csv(r"C:\Users\yanqinchen\Desktop\jetcost_clicks.csv",index=False)