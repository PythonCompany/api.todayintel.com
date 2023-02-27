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
from selenium.webdriver.support import expected_conditions as EC

# Allows us to use keyboard keys
from selenium.webdriver.common.keys import Keys
import time

username = "nomaxvalue"                # Enter in your email for Instagram inside the quotation marks
mypassword = "garcelino87#"             # Enter in your password for Instagram inside the quotation marks
friendusernames = ["alina_kiss_aa"]      # Enter in the username of the recipient inside the quotation marks! To send this to mutiple users, seperate users by commas! Ex)  friendusernames = ["@friend1", "@friend2", "@friend3"]
numoftimes = "1"             # Enter in the number of times you would like to send the message to the recipient Ex) "2"

# The message being sent
message = ""

PATH = "/usr/bin/chromedriver"                   # Step 4 of the installations instructions

driver = webdriver.Chrome(PATH)

url = "https://www.instagram.com/"
driver.get(url)

try:
    try:
        dmbtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '._a9_0')))
        dmbtn.click()
    except:
        print ("Could not find the allow cookies button")

    try:
        # Waits for the login box to appear on the webpage
        usernamebox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        # Login to Instagram
        usernamebox.send_keys(username)
        passwordbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
        passwordbox.send_keys(mypassword)

        #Todo add the login button
        loginbutton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
        loginbutton.click()
        print("Logging in")
    except:
        print("Could not login!")

    try:
        dmbtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[4]/div/a')))
        dmbtn.click()
    except:
        print ("Could not find or click the direct message button")

    try:
        notificationsnotnow = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')))
        notificationsnotnow.click()
    except:
        print ("Could not click not now on the notifications pop up!")

    for friendusername in friendusernames:
        try:
            searchuser = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div/div[3]/div/button')))
            searchuser.click()
        except:
            print ("Could not click on the new message button!")
        try:
            searchuserbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'queryBox')))
            searchuserbox.send_keys(friendusername)
        except:
            print ("Could not find the enter username box!")

        try:
            time.sleep(2)
            firstuser = driver.find_element_by_css_selector('.HVWg4')
            firstuser.click()
        except:
            print("Could not click on the first user!")

        try:
            pressingnext = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rIacr')))
            pressingnext.click()
        except:
            print ("Could not press \"Next\"!")

        try:
            messagebox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.focus-visible')))
            messagebox.click()
        except:
            print ("Could not find the text box!")

        try:
            # Finds the text box
            textbox = driver.find_element_by_css_selector('.focus-visible')
        except:
            print("Could not find the text box!")

        try:
            # Sends the message
            for i in range(int(numoftimes)):
                textbox.send_keys(message)
                textbox.send_keys(Keys.RETURN)
        except:
            print("Error sending the message!")

except:
    print("An error has occurred")
    time.sleep(1)
    driver.quit()