import json
import datetime
import os
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

URL = "https://www.saucedemo.com/"
USERS = ["standard_user", "locked_out_user", "problem_user", "performance_glitch_user", "error_user", "visual_user", "invalid_user"]
PASSWORD = "secret_sauce"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE_NAME = 'loginTestResults.json'
OUTPUT_PATH = os.path.join(ROOT_DIR, OUTPUT_FILE_NAME)
results = []

try:
    driver = webdriver.Chrome()
    driver.get(URL)
    for item in USERS:
        try:
            result = {}
            result['username'] = item
            result['test_start'] = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            #user
            driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[1]/div/div/form/div[1]/input").send_keys(item)
            #password
            driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[1]/div/div/form/div[2]/input").send_keys(PASSWORD)
            #click login
            driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[1]/div/div/form/input").click()

            #check for error popup
            try:
                errorMessage = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[1]/div/div/form/div[3]/h3").get_attribute('innerHTML')
                if ("locked" in errorMessage):
                    print("This user is locked out: " + item)
                    result['error_message'] = "Locked out"
                elif ("match" in errorMessage):
                    print("This user doesn't match any user in the database: " + item)
                    result['error_message'] = "Invalid user"
                else:
                    print("Unknown error: " + item)
                    result['error_message'] = "Unknown"
                result['correct'] = False
                driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[1]/div/div/form/div[1]/input").send_keys(Keys.CONTROL + "a")
                driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[1]/div/div/form/div[1]/input").send_keys(Keys.DELETE)
                driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[1]/div/div/form/div[2]/input").send_keys(Keys.CONTROL + "a")
                driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[1]/div/div/form/div[2]/input").send_keys(Keys.DELETE)
                
            except NoSuchElementException:
                #succesful login
                result['correct'] = True
                result['error_message'] = ""
                #click burger menu
                driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[1]/div[1]/div/div[1]/div/button").click()
                #click logout
                driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/nav/a[3]").click()
        except:
            print("Error with item " + item)
        finally:
            result['test_end'] = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            results.append(result)

except:
    print("Connection error")
finally:
    print("Testing ended, closing driver")
    driver.close()
    print("Writing results to file " + OUTPUT_PATH)
    with open(OUTPUT_PATH, 'w') as outfile:
        outfile.write(json.dumps(results))
