# import required packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# start the selenium browser session
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://sunbeaminfo.in/internship")

WebDriverWait(driver, 10).until(EC.title_contains("Sunbeam"))

print("Page Title:", driver.title)

table_body = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "table.table.table-bordered.table-striped")
    )
)

table_rows = table_body.find_elements(By.TAG_NAME, "tr")

for row in table_rows[1:]:  # skip header row
    cols = row.find_elements(By.TAG_NAME, "td")
    
    if len(cols) >= 8:
        info = {
            "Sr.No": cols[0].text,
            "Batch": cols[1].text,
            "Batch Duration": cols[2].text,
            "Start Date": cols[3].text,
            "End Date": cols[4].text,
            "Time": cols[5].text,
            "Fees (Rs.)": cols[6].text,
            "Download Brochure": cols[7].text
        }
        print(info)

driver.quit()