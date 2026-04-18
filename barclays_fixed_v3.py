
import json, time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('config.json') as f:
    cfg = json.load(f)

resume_path = os.path.abspath(cfg['resume_path'])
job_url = cfg['job_urls'][0]

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)

print(f"Opening {job_url}")
driver.get(job_url)

print("\n=== STEP 1: LOG IN MANUALLY ===")
print("Complete login, MFA, CAPTCHA in the browser.")
input("Press ENTER after you see the application page...")

# Try to upload resume - improved for Workday 2025/2026
print("\nLooking for resume upload...")
uploaded = False
for attempt in range(20):
    try:
        # Find all file inputs, including hidden
        inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
        for inp in inputs:
            try:
                driver.execute_script("arguments[0].style.opacity = 1; arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';", inp)
                inp.send_keys(resume_path)
                print(f"✓ Resume sent to hidden input (attempt {attempt+1})")
                uploaded = True
                break
            except: pass
        if uploaded: break
        # If no input found, try clicking upload buttons
        buttons = driver.find_elements(By.XPATH, "//button[contains(.,'Upload') or contains(.,'Select') or contains(.,'My Device') or contains(.,'Browse')]")
        for b in buttons[:2]:
            try:
                driver.execute_script("arguments[0].click();", b)
                time.sleep(1)
            except: pass
    except: pass
    time.sleep(1.5)

if not uploaded:
    print("Could not auto-upload. Please drag-drop resume.pdf manually.")
else:
    print("Upload triggered. Wait for Workday to parse (30-60s)...")
    time.sleep(10)

print("\n=== DONE ===")
print("Browser stays open. Fill remaining fields. The script saved you the login wait and attempted upload.")
