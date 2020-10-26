''' ------------------------------------------------------------------
 Project        : Webscraping AIR India wesbite for Speech Data.
 Author         : S.Moris
 Organization   : Indian Institute of Information Technology
 --------------------------------------------------------------------'''
 # Importing Necessary libraries.
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
# URL for scraping the Transcript data
url = 'http://newsonair.com/RNU-NSD-Audio-Archive-Search.aspx'
# Set chrome profile
ChromeOptions = Options()
ChromeOptions.add_experimental_option("prefs",{"download.default_directory":"Z:\Python\Audio"})
driver = webdriver.Chrome(executable_path='Z:/Python/chromedriver_win32/chromedriver.exe',chrome_options=ChromeOptions)
driver.implicitly_wait(30)
print("[INFO] The Chrome Profile has been created and the session will commence now.")
# SET variables for the website:
NSD_TYPE = 'Regional'
NSD_Region = 'Itanagar'
NSD_Language = 'Hindi'
NSD_Bulletin = '1645'
# Change the variables to download other audio archive.
''' Create a dataframe to keep the texts'''
Dates = []
# Functions for doing various stuff.
def PageInitialization():
    driver.get(url)
    driver.implicitly_wait(10)
    #Click the Main Broadcast archive button
    MianBroadcast_Button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_program_type_cbl_0")
    MianBroadcast_Button.click()
    #Wait 10 seconds for the website to load
    driver.implicitly_wait(10)
    Type = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwtype'))
    Type.select_by_visible_text(NSD_TYPE)
    Region = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsdname'))
    Region.select_by_visible_text(NSD_Region)
    Language = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwlanguages'))
    Language.select_by_visible_text(NSD_Language)
    Bulletin = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsd_bname'))
    Bulletin.select_by_visible_text(NSD_Bulletin)
    # Press the find button to get the text  files.
    find_button = driver.find_element_by_id('ctl00_ContentPlaceHolder1_Button1')
    find_button.click()
    driver.implicitly_wait(10)

def GetLinkAndDate():
    # Empty dictionary for storing link and Name
    Dictionary = {}
    # Find all the source link by 'audio' tag and store the src link.
    links = driver.find_elements_by_tag_name('audio')
    #ctl00_ContentPlaceHolder1_RepterDetails_ctl00_HyperLink2
    row = ["%.2d" % i for i in range(0,30)]
    stringOne ='ctl00_ContentPlaceHolder1_RepterDetails_ctl'
    stringTwo = '_HyperLink2'
    #print(len(links))
    i =0
    for link in links:
        source = link.get_attribute('src')
        date = (driver.find_element_by_id(stringOne+str(row[i])+stringTwo).text)
        Dictionary[date]=source
        i = i +1
    return Dictionary


def LoopForPages():
    page = True
    num = 2
    while(page):
        dic = GetLinkAndDate()
        for key in dic.keys():
            URL = dic[key]
            name = directory + key + '.mp3'
            wget.download(URL,name)
            print('Donwloaded :',name)
            time.sleep(10)
        try:
          #ctl00_ContentPlaceHolder1_lbLast
          next = driver.find_element_by_link_text(str(num))
          next.click()
          print('Next Page is found')
          num = num + 1
        except:
          print('Next page is not found')
          page = False
''' ---------------------------Perform the looping task----------------------------------------'''
directory = 'Z:/Python/Audio/'
PageInitialization()
LoopForPages()

