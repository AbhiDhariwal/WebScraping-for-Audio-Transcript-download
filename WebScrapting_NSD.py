''' -----------------------------------------------------------------------
 Project        : Webscraping AIR India wesbite for NSD Transcript.
 Author         : S.Moris
 Organization   : Indian Institute of Information Technology
 ----------------------------------------------------------------------------'''
 # Importing Necessary libraries.
from selenium import webdriver
import wget
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
# URL for scraping the audio data.
url = 'http://newsonair.com/RNU-NSD-Audio-Archive-Search.aspx'
# Set chrome profile
ChromeOptions = Options()
ChromeOptions.add_experimental_option("prefs",{"download.default_directory":"Z:\Python\Transcript"})
driver = webdriver.Chrome(executable_path='Z:/Python/chromedriver_win32/chromedriver.exe',chrome_options=ChromeOptions)
#ctl00_ContentPlaceHolder1_program_type_cbl
driver.implicitly_wait(30)
driver.get(url)
print("[INFO] The Chrome session has been started.")
#Click the Main Broadcast archive button
MianBroadcast_Button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_program_type_cbl_1")
MianBroadcast_Button.click()
#Wait 10 seconds for the website to load
driver.implicitly_wait(10)
# Select Options for Finding Transcript;
NSD_Type = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwtype'))
NSD_Type.select_by_visible_text('Regional')
NSD_Region = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsdname'))
NSD_Region.select_by_visible_text('Itanagar')
NSD_Language = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwlanguages'))
NSD_Language.select_by_visible_text('Hindi')
NSD_Bulletin = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsd_bname'))
NSD_Bulletin.select_by_visible_text('1645')
# Press the find button to get the text  files.
find_button = driver.find_element_by_id('ctl00_ContentPlaceHolder1_Button1')
find_button.click()
#Wait 10 seconds for the website to load
print('[INFO] The website has been loaded, now searching links.')
driver.implicitly_wait(10)
# FInd  all the  Download Link :
download = driver.find_elements_by_link_text('Download')
for link in download:
    link.click()
    driver.implicitly_wait(2) # wait for 2 seconds

driver.implicitly_wait(10)# Wait 10 seconds before closing.