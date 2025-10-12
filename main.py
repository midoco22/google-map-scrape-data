from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument("--lang=en-US")
options.add_argument('disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

url = "https://www.google.com/maps/search/schools+near+raipur+lakhsmipur/?hl=en"
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(url)
sleep(7)

data = []

try:
    urls = []

    containers = driver.find_elements(By.CSS_SELECTOR, ".hfpxzc")
    for container in containers:
        link = container.get_attribute("href")
        if link:
            urls.append(link)

    print(f"Number of Schools found: {len(urls)}")
        
    for i in range(len(urls)):
        driver.get(urls[i])
        sleep(10)

        try:
            name = driver.find_element(By.CSS_SELECTOR, ".DUwDvf").get_attribute("innerText")
        except:
            name = "N/A"
        try:
            phone = driver.find_element(By.XPATH, "//button[@data-tooltip='Copy phone number']").text.replace("\n","")
        except:
            phone = "N/A"
        try:
            address = driver.find_element(By.XPATH, "//button[@data-tooltip='Copy address']").text.replace("\n","")
        except:
            address = "N/A"
        try:
            website = driver.find_element(By.XPATH, "//a[@data-tooltip='open website']").get_attribute('href')
        except:
            website = "N/A"
        try:
            ratings = driver.find_element(By.CSS_SELECTOR, ".F7nice").get_attribute("aria-label")
        except:
            ratings = "N/A"
            
        data.append({
            "Name": name,
            "Phone": phone,
            "Address": address,
            "Website": website,
            "Ratings": ratings,
        })

except Exception as e:
    print(f"Error extracting data: {e}")

finally:
    driver.quit()


df = pd.DataFrame(data)
print(df.to_string())

df.to_csv("schools_raipur_lakhsmipur.csv", index=False)