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
import time
from os import path
import os
from pydub import AudioSegment
import glob
import pandas as pd 
import shutil
# Read the .csv file
data = pd.read_csv('AudioData.csv')
data = data.values
#print(data)
# URL for scraping the Transcript data
url = 'http://newsonair.com/RNU-NSD-Audio-Archive-Search.aspx'
# Set chrome profile
ChromeOptions = Options()
ChromeOptions.add_experimental_option("prefs",{"download.default_directory":"/home/luvitusmaximus/Documents/ASR/Audio"})
driver = webdriver.Chrome(executable_path='/home/luvitusmaximus/Documents/ASR/chromedriver',chrome_options=ChromeOptions)
driver.implicitly_wait(30)
print('\n\n')
print("[INFO] The Chrome Profile has been created and the session will commence now.")
''' Functions to different job --------'''
def PageInitialization(t,r,l,b):
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(1) # make 10 while running
    #Click the Main Broadcast archive button
    MianBroadcast_Button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_program_type_cbl_0")
    MianBroadcast_Button.click()
    #Wait 10 seconds for the website to load
    driver.implicitly_wait(10)
    Type = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwtype'))
    Type.select_by_visible_text(t)
    driver.implicitly_wait(10)
    Region = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsdname'))
    Region.select_by_visible_text(r)
    driver.implicitly_wait(10)
    Language = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwlanguages'))
    Language.select_by_visible_text(l)
    driver.implicitly_wait(10)
    Bulletin = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddwrnunsd_bname'))
    Bulletin.select_by_visible_text(b)
    driver.implicitly_wait(10)
    # Press the find button to get the text  files.
    find_button = driver.find_element_by_id('ctl00_ContentPlaceHolder1_Button1')
    find_button.click()
    driver.implicitly_wait(10)
    
def GetLinkAndDate():
    time.sleep(5)
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
        #print(stringOne+str(row[i])+stringTwo)
        try:
            date = driver.find_element_by_id(stringOne+str(row[i])+stringTwo).text
        except:
            break
        #print("Date :",date,'\n')
        Dictionary[date]=source
        i = i +1
    return Dictionary

def LoopForPages(r,t):
    page = True
    num = 2
    while(page):
        dic = GetLinkAndDate()
        for key in dic.keys():
            URL = dic[key]
            name = directory + r +' ' + t + ' ' + key + '.mp3' # Example Itanagar 1645 03 Oct 2020.mp3
            #wget.download(URL,name)
            print('Donwloaded :',name)
            time.sleep(1) # make 15 while running .
        try:
          #ctl00_ContentPlaceHolder1_lbLast
          next = driver.find_element_by_link_text(str(num))
          next.click()
          print('\n\n[INFO] Next Page is found')
          num = num + 1
        except:
          print('\n\n[INFO] Next page is not found,quitting now')
          page = False

directory ='/home/luvitusmaximus/Documents/ASR/Audio/'
for region in range(0,len(data)):
    # SET variables for the website:
    NSD_TYPE        =  data[region][0]
    NSD_Region      =  data[region][1]
    NSD_Language    =  data[region][2]
    bulletin        =  str(data[region][3])
    if len(str(data[region][3]))==3:
        bulletin = '0'+str(data[region][3])
    NSD_Bulletin    =  bulletin
    print(data[0])
    PageInitialization(NSD_TYPE,NSD_Region,NSD_Language,NSD_Bulletin)
    LoopForPages(NSD_Region,NSD_Bulletin)
    driver.close()
time.sleep(10)
#driver.close()
'''--------- COnvert to .wav--------------'''
filenames = glob.glob('/home/luvitusmaximus/Documents/ASR/'+'*')
for src in filenames:
    sound = AudioSegment.from_mp3(src)
    sound = sound.set_channels(1)
    var = src.split('.')
    dst = var[0]
    sound.export(dst, format="wav",bitrate='16k') # mp3 file --> sin(1khz) + sin(20khz)
    os.remove(src)