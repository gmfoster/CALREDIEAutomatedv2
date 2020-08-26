# Selenium is the package that allows us to automate a web browser
from selenium import webdriver

# Pandas lets us open, save, and close the TSV file (this is the same as opening and saving in excel, should solve the problem)
import pandas as pd

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
from os import path
from datetime import date

# The location you want the data set from calredie downloaded into
# r before the string allows us to use original file paths without converting to /
download_directory = r'C:\Users\fosterg\Desktop\CALREDIEAutomated-master\Data'

# The location of your R script (make sure the R script is pointed at the download_directory
r_script_location = r'C:\Users\fosterg\Desktop\CALREDIEAutomated-master\R_scripts\covid19_ddp_full_dashboard_ver3.R'

# Where Rscript.exe is located on your machine ( path/R/R-4.0.2/bin/Rscript)
rScript = r'C:\Users\fosterg\Documents\R\R-4.0.2\bin\Rscript'

# Your Username/Password pair
username = "44GFosterNCOV"
password = "Welcome2020c1"


class CalredieAutomator:
    def __init__(self):

        # CalREDIE Sign On Info
        self.username = username
        self.password = password

        # Wherever the R script is located on your machine
        self.script_location = r_script_location

        # Initialize Options
        self.options = Options()
        self.options.headless = True # headless = True hides the chrome browser running in the background, set this to
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

    def click_through_systems_tab_exports(self):
        '''
        This function navigates through the calredie sight and downloads all disease grouping incidents up to the current date
        '''

        # # Check for page load
        # while True:
        #     try:
        #         WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$btnExtracts")))
        #         break
        #     except TimeoutException:
        #         print("Timeout Exception: Page element took too long to load")
        #
        # # Click Extracts
        # self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnExtracts").click()
        # print("DEBUG: clicked extracts")

        # Check for page load
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$btnSysTab")))
                break
            except TimeoutException:
                print("Timeout Exception: Page element took too long to load")
        # Systems tab exports click begin
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnSysTab").click()
        print("DEBUG: clicked exports")

        # Check for page load
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$btnCreate")))
                break
            except TimeoutException:
                print("Timeout Exception: Page element took too long to load")
        # Export all disease grouping incidents
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnCreate").click()
        print("DEBUG: clicked export all disease grouping incidents")

        # Check for page load
        while True:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$txtStart")))
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder1$txtEnd")))
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                    (By.XPATH, "//select[@id='ContentPlaceHolder1_ddDateType']/option[3]")))
                break
            except TimeoutException:
                print("Timeout Exception: Page element took too long to load")
        # Date type: episode date
        self.driver.find_element_by_xpath("//select[@id='ContentPlaceHolder1_ddDateType']/option[3]").click()
        print("DEBUG: select from dropdown menu")

        # Start Date
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtStart").send_keys("1/4/2010")
        print("DEBUG: entered start date")

        # End Date
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtEnd").send_keys(self.todays_date)
        print("DEBUG: entered end date")

        # Download
        self.driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnCreate").click()
        print("DEBUG: downloading")

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

    def run_R_script(self):
        '''
        This function runs the specified R script
        :return: Null
        '''

        # Check if the file exists, if not (hasn't finished downloading) sleep for 5 seconds and check again
        while not path.exists(download_directory + r'/UDF_Disease_Data.tsv'):
            time.sleep(5)

        while not path.exists(download_directory + r'/DiseaseCountyDisGrpData.tsv'):
            time.sleep(5)

        # Execute R script
        #subprocess.check_call([rScript, self.script_location], shell=False)

        subprocess.call("C:/Users/fosterg/Documents/R/R-4.0.2/bin/Rscript --vanilla C:/Users/fosterg/Desktop/CALREDIEAutomated-master/R_scripts/covid19_ddp_full_dashboard_ver3.R", shell=True)


    def handle_file_encoding(self):
        while not path.exists(download_directory + r'/UDF_Disease_Data.tsv'):
            time.sleep(5)

        r_fileTSV = download_directory + r'/UDF_Disease_Data.tsv'
        w_fileTSV = download_directory + r'/UDF_Disease_Data.tsv'
        UDF_read = pd.read_csv(r_fileTSV, sep='\t')


        with open(w_fileTSV, 'w') as write_tsv:
            write_tsv.write(UDF_read.to_csv(sep='\t', index=False, encoding='latin-1'))
