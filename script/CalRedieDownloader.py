# Selenium is the package that allows us to automate a web browser
from selenium import webdriver

# Webdriver_manager assures we have the correct chromedriver for selenium to work, if we dont, it downloads it.
from webdriver_manager.chrome import ChromeDriverManager

# Options allows us to change the webdriver options like managing downloads or hiding the browser window
from selenium.webdriver.chrome.options import Options

# For error handling
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Subprocess allows us to run an R script from within a python script
import subprocess

import time
import os
from os import path
from datetime import date

# The location you want the data set from calredie downloaded into
# r before the string allows us to use original file paths without converting to /
#download_directory = r'C:\Users\fosterg\Desktop\CALREDIEAutomated-master\Data'
download_directory = r'I:\Shared\Epi Unit\4. Cross Training\COVID-19\CalREDIE Data Downloads\Autodownload_Test'

# Your Username/Password pair
username = "44GFosterNCOV"
password = "Welcome2020c1"


class CalredieDownloader:
    def __init__(self):

        # CalREDIE Sign On Info
        self.username = username
        self.password = password


        # Initialize Options
        self.options = Options()
        self.options.headless = False # headless = True hides the chrome browser running in the background, set this to
        # false if you want to watch the script step through the website
        prefs = {'download.default_directory': download_directory}
        self.options.add_experimental_option('prefs', prefs)

        # Get and format todays date
        self.today = date.today()
        self.todays_date = self.today.strftime("%m/%d/%Y")

        # Initialize webdriver
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)

        # if page takes longer than 15 seconds to load it times out...
        self.driver.set_page_load_timeout(15)

    def load(self):
        '''
        Load calredie web site
        :return: Null
        '''
        self.driver.get("https://calredie.cdph.ca.gov/CalREDIE_Export/login.aspx?ReturnUrl=%2fCalREDIE_Export%2f")

    def login(self):
        '''
        This functions locates the username/password fields, enters specified username/password combo and clicks login
        :return: Null
        '''

        # This block waits until the username/password and login fields are loaded before proceeding
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$MyLogin$UserName")))
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$MyLogin$Password")))
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$MyLogin$LoginButton")))
                break
            except TimeoutException:
                print("Timeout Exception: Page elements took too long to load")

        # Find username field
        login_field = self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$MyLogin$UserName")

        # Enter username
        login_field.send_keys(self.username)
        print("DEBUG: entered username")

        # Find password field
        password_field = self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$MyLogin$Password")

        # Enter password
        password_field.send_keys(self.password)
        print("DEBUG: entered password")

        # Find login button
        login_button = self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$MyLogin$LoginButton")

        # Login
        login_button.click()
        print("DEBUG: clicked login")

    def click_through_udf_data_exports(self):
        # Wait for extracts page to load
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$btnUDF")))
                break
            except TimeoutException:
                print("Timeout Exception: Page element took too long to load")
        # Complete UDF data extracts: begin
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnUDF").click()

        # Check For Page Load
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$RBDiseaseGrp")))
                break
            except TimeoutException:
                print("Timeout Exception: Page element took too long to load")
        # Select NCOV2019
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$RBDiseaseGrp").click()

        # Click Begin
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$BtnBegin").click()

        # Check For Page Load
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='ContentPlaceHolder1_ddDisease']/option[3]")))
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='ContentPlaceHolder1_ddDateType']/option[3]")))
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$txtStart")))
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$txtEnd")))
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$btnBegin")))

                break
            except TimeoutException:
                print("Timeout Exception: Page element took too long to load")

        # Select Disease: Novel Coronavirus 2019
        self.driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_ddDisease']/option[3]").click()

        # Select Date Type: Episode Date
        self.driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_ddDateType']/option[3]").click()

        # Start Date: 1/4/2010
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtStart").send_keys("1/4/2010")

        # End Date: Todays Date
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtEnd").send_keys(self.todays_date)

        # Click Begin/Download
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnBegin").click()

    def extracts(self):
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='TreeView1t1']")))
                break
            except TimeoutException:
                print("Timeout Exception: Page element took too long to load")
        self.driver.find_element_by_xpath("//*[@id='TreeView1t1']").click()

        # Check for page load
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$btnExtracts")))
                break
            except TimeoutException:
                print("Timeout Exception: Page element took too long to load")
        # Click Extracts
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnExtracts").click()
        print("DEBUG: clicked extracts")

    def close(self):
        '''
        This function closes the web browser
        :return: Null
        '''
        self.driver.close()

    def rename(self):
        print("DEBUG: Renaming")
        oldFile = 'I:/Shared/Epi Unit/4. Cross Training/COVID-19/CalREDIE Data Downloads/Autodownload_Test/UDF_Disease_Data.tsv'
        count = 0
        while not path.exists(oldFile):
            print("DEBUG: File Doesnt Exist Yet, Sleeping")
            time.sleep(5)
            count += 1
            if count > 30:
                print("ERROR: File took to long to download, exiting")
                return 0
        date = self.today.strftime("%m-%d-%Y")
        newFile = 'I:/Shared/Epi Unit/4. Cross Training/COVID-19/CalREDIE Data Downloads/Autodownload_Test/UDF_Disease_Data_' + date + '.tsv'

        os.rename(oldFile, newFile)
        # if path.exists(oldFile):
        #     print("old file still exists")
        #     os.remove(oldFile)

    def checkExist(self):
        date = self.today.strftime("%m-%d-%Y")
        newFile = 'I:/Shared/Epi Unit/4. Cross Training/COVID-19/CalREDIE Data Downloads/Autodownload_Test/UDF_Disease_Data_' + date + '.tsv'
        return path.exists(newFile)

if __name__ == "__main__":
    automator = CalredieDownloader()
    if automator.checkExist():
        print("Dataset from " + str(automator.today) + " already exists, closing")
        automator.close()
    else:
        automator.load()
        automator.login()
        automator.extracts()
        automator.click_through_udf_data_exports()
        automator.rename()
        automator.close()