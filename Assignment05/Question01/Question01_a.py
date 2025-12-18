from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ----------------- SETUP -----------------
chrome_options = Options()
chrome_options.add_argument("--headless")  # remove if you want to see browser
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

# ----------------- LOAD PAGE -----------------
driver.get("https://sunbeaminfo.in/internship")

# Scroll to bottom to load dynamic content
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# ----------------- CLICK TO EXPAND TABLE -----------------
plus_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='#collapseSix']"))
)
driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
plus_button.click()

# Wait for table to load
table = wait.until(
    EC.presence_of_element_located((By.XPATH, "//div[@id='collapseSix']//table"))
)

# ----------------- READ TABLE -----------------
table_body = table.find_element(By.TAG_NAME, "tbody")
table_rows = table_body.find_elements(By.TAG_NAME, "tr")

print("\n📋 Internship Program Details:\n")

for row in table_rows:
    cols = row.find_elements(By.TAG_NAME, "td")

    if len(cols) >= 4:
        info = {
            "Technology": cols[0].text,
            "Aim": cols[1].text,
            "Prerequisite": cols[2].text,
            "Learning Location": cols[3].text
        }
        print(info)

driver.quit()