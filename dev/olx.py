'''
By: Donald Lee
Date: August 10th-13th, 2020

For instructions or information, please refer to https://github.com/Donald-K-Lee/InstagramDMBot/blob/master/README.md

Please do NOT use this for spam, bullying, etc.
By using this script, YOU will take FULL responsibility for anything that happens to ANYONE you use this on and anything you do with this script!.
Additionally, using this script may involve a risk of you being banned and even other risks including but not limited to: being hacked, etc.
Use this script at your own risk!
'''

from selenium import webdriver
# To wait for side load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from selenium.webdriver.support import expected_conditions as EC

# Allows us to use keyboard keys
from selenium.webdriver.common.keys import Keys
import time

username = ""                # Enter in your email for Instagram inside the quotation marks
mypassword = ""             # Enter in your password for Instagram inside the quotation marks
friendusernames = ["alina_kiss_aa"]      # Enter in the username of the recipient inside the quotation marks! To send this to mutiple users, seperate users by commas! Ex)  friendusernames = ["@friend1", "@friend2", "@friend3"]
numoftimes = "1"             # Enter in the number of times you would like to send the message to the recipient Ex) "2"

# The message being sent
message = ""

PATH = "/usr/bin/chromedriver"                   # Step 4 of the installations instructions

driver = webdriver.Chrome(PATH)

url = "https://www.olx.ro/d/oferta/transport-persoane-germania-la-adresa-IDeFjlS.html"
driver.get(url)

try:
    #/html/body/div[3]/div[3]/div/div[1]/div/div[2]/div/button[1]

    try:
        dmbtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div[1]/div/div[2]/div/button[1]')))
        dmbtn.click()
    except:
        print ("Could not find accept cookies button")
    try:
        dmbtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[3]/div[3]/div[2]/div[1]/div[3]/div/button[1]')))
        dmbtn.click()
        time.sleep(15)
        dmbtn.until(EC.element_to_be_clickable(By.XPATH,'/html/body/div[2]/div[1]/div[3]/div[3]/div[2]/div[1]/div[3]/div/button[1]/span/a'))
        print(dmbtn.getText())

    except:
        print ("Could not find call button")


except:
    print("An error has occurred")
    time.sleep(1)
    driver.quit()
