from selenium import webdriver
import wget
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os
import shutil
import glob
import datetime
import time
from tqdm import tqdm

# =============================================================================
###              Settings
# =============================================================================
chrome_dirver_path = 'C:/Users/COOLA/chromedrive_90/chromedriver.exe'
download_dir = r"G:\download\news_on_air_data"

# URL for scraping the Transcript data
url = 'http://newsonair.com/RNU-NSD-Audio-Archive-Search.aspx'
# Set chrome profile
ChromeOptions = Options()
ChromeOptions.add_experimental_option("prefs",{"download.default_directory":download_dir})

driver = webdriver.Chrome(executable_path=chrome_dirver_path, chrome_options=ChromeOptions)
driver.implicitly_wait(5)

print("[INFO] The Chrome Profile has been created and the session will commence now.")


# =============================================================================
# functions
# =============================================================================


# Change the variables to download other audio archive.
''' Create a dataframe to keep the texts'''
Dates = []
# Functions for doing various stuff.
def PageInitialization(NSD_TYPE,NSD_Region,NSD_Language,NSD_Bulletin,wait = 20,fromDate="01/01/2011"):
    driver.get(url)
    driver.implicitly_wait(wait)
    #Click the Main Broadcast archive button
    MianBroadcast_Button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_program_type_cbl_0")
    MianBroadcast_Button.click()
    #Waiting for the website to load
    driver.implicitly_wait(wait)
    Type = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwtype'))
    Type.select_by_visible_text(NSD_TYPE)
    driver.implicitly_wait(3)
    Region = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsdname'))
    Region.select_by_visible_text(NSD_Region)
    driver.implicitly_wait(3)
    Language = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwlanguages'))
    Language.select_by_visible_text(NSD_Language)
    driver.implicitly_wait(3)
    Bulletin = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsd_bname'))
    Bulletin.select_by_visible_text(NSD_Bulletin)
    driver.implicitly_wait(3)
    fromDateButton = driver.find_element_by_id('ctl00_ContentPlaceHolder1_from_Date_txt')
    # fromDate = "1/12/2010 8:20:37 PM"
    # fromDate = "01/01/2011"
    fromDateButton.clear()
    fromDateButton.send_keys(fromDate)
    driver.implicitly_wait(3)
    # Press the find button to get the text  files.
    find_button = driver.find_element_by_id('ctl00_ContentPlaceHolder1_Button1')
    find_button.click()
    driver.implicitly_wait(wait)

def GetLinkAndDate():
    # Empty dictionary for storing link and Name
    Dictionary = {}
    # Find all the source link by 'audio' tag and store the src link.
    links = driver.find_elements_by_tag_name('audio')
    #ctl00_ContentPlaceHolder1_RepterDetails_ctl00_HyperLink2
    # row = ["%.2d" % i for i in range(0,25)]
    # stringOne ='ctl00_ContentPlaceHolder1_RepterDetails_ctl'
    # stringTwo = '_HyperLink2'
    #print(len(links))
    
    ##update over earlier method as it take long time to check each url where related data is not present as cost of Datetime
    ## can be managed through audio file name has datatime embedded in them
    i =0
    for link in tqdm(links[:]):
        source = link.get_attribute('src')
        if NSD_Region in source:
            # date = (driver.find_element_by_id(stringOne+str(row[i])+stringTwo).text)
            key = source.split("/")[-1]
            Dictionary[key]=source
            i = i +1
       
    return Dictionary



def LoopForPages(sleep = 5,download=False):
    downloadDict = {}
    page = True
    num = 2
    while(page):
        try:
            start = time.time()
            dic = GetLinkAndDate()
            end = time.time()
            for key in dic.keys():
                URL = dic[key]
                name = directory + key 
                if download:
                    wget.download(URL,name)
                    print('Donwloaded :',name)
                downloadDict[name] = URL
                
                # time.sleep(3)
            try:
              #ctl00_ContentPlaceHolder1_lbLast
              next = driver.find_element_by_link_text(str(num))
              next.click()
              print('Next Page is found')
              num = num + 1
            except:
              print('Next page is not found')
              page = False
              end = time.time()
              
            print(len(downloadDict),end-start)
            time.sleep(sleep)
        except:
            print("eror",num,key)
    return downloadDict
        

# =============================================================================
#           option menu details on website
# =============================================================================

extract_lang = "Hindi"

import pandas as pd

audio_df = pd.read_csv("AudioData.csv")

lang_df = audio_df[audio_df.NSD_Language == extract_lang]

final_data = []

for index,row in lang_df.iterrows():
    # SET variables for the website:
    if True:
        NSD_TYPE = row.NSD_TYPE
        NSD_Region = row.NSD_Region
        NSD_Language = row.NSD_Language
        NSD_Bulletin = str(row.NSD_Bulletin)
        if len(NSD_Bulletin)<4:
            NSD_Bulletin = "0"+NSD_Bulletin
        directory = 'G:/download/'
        PageInitialization(NSD_TYPE,NSD_Region,NSD_Language,NSD_Bulletin,wait=60)
        downloadDict = LoopForPages(7)
        w = {
            "NSD_TYPE":NSD_TYPE,
            "NSD_Region":NSD_Region,
            "NSD_Language":NSD_Language,
            "NSD_Bulletin":NSD_Bulletin,
            "download_paths":downloadDict
            }
        final_data.append(w)

        fd = pd.DataFrame(final_data)
        
        
        fd.to_csv(f"NewsOnAir_{extract_lang}.csv")



        
''' ---------------------------Perform the looping task----------------------------------------'''



# driver.get(url)
# driver.implicitly_wait(10)
# #Click the Main Broadcast archive button
# MianBroadcast_Button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_program_type_cbl_0")
# MianBroadcast_Button.click()
# #Wait 10 seconds for the website to load
# driver.implicitly_wait(10)
# Type = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwtype'))
# Type.select_by_visible_text(NSD_TYPE)
# Region = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsdname'))
# Region.select_by_visible_text(NSD_Region)
# Language = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwlanguages'))
# Language.select_by_visible_text(NSD_Language)
# Bulletin = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsd_bname'))
# Bulletin.select_by_visible_text(NSD_Bulletin)
# fromDateButton = driver.find_element_by_id('ctl00_ContentPlaceHolder1_from_Date_txt')
# fromDate = "5/20/2020 8:20:37 PM"
# fromDateButton.clear()
# fromDateButton.send_keys("5/20/2020 8:20:37 PM")


# # fromDate = "5/24/2020 8:20:37 PM"
# # Bulletin.select_by_visible_text(fromDate)

# # Press the find button to get the text  files.
# find_button = driver.find_element_by_id('ctl00_ContentPlaceHolder1_Button1')
# find_button.click()
# driver.implicitly_wait(10)

