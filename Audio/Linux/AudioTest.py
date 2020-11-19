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
import argparse
# URL for scraping the Transcript data
url = 'http://newsonair.com/RNU-NSD-Audio-Archive-Search.aspx'
# Set chrome profile
ChromeOptions = Options()
ChromeOptions.add_experimental_option("prefs",{"download.default_directory":"/home/luvitusmaximus/Documents/ASR/Audio"})
driver = webdriver.Chrome(executable_path='/home/luvitusmaximus/Documents/ASR/chromedriver',chrome_options=ChromeOptions)
driver.implicitly_wait(30)
print('\n\n')
print("[INFO] The Chrome Profile has been created and the session will commence now.")
# Setting argument Parser
parser = argparse.ArgumentParser()
# Setup variables through parser.
parser.add_argument('--t','-nsdType',type=str,default='Regional',help='NSD Regional type.')
parser.add_argument('--r','-nsdRegion',type=str,default='Itanagar',help='NSD Region to collect audio from.')
parser.add_argument('--l','-nsdLanguage',type=str,default='Hindi',help='NSD Language.')
parser.add_argument('--b','-nsdBulletin',type=str,default='1645',help='NSD Regional type.')
# Pass the argumets
args = parser.parse_args()
# SET variables for the website:
NSD_TYPE        = args.t
NSD_Region      = args.r
NSD_Language    = args.l
NSD_Bulletin    = args.b
# Change the variables to download other audio archive.
''' Create a dataframe to keep the texts'''
Dates = []
# Functions for doing various stuff.
def PageInitialization():
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(1) # make 10 while running
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
    time.sleep(5)
    # Empty dictionary for storing link and Name
    Dictionary = {}
    # Find all the source link by 'audio' tag and store the src link.
    links = driver.find_elements_by_tag_name('audio')
    #ctl00_ContentPlaceHolder1_RepterDetails_ctl00_HyperLink2
    row = ["%.2d" % i for i in range(0,30)]
    stringOne ='ctl00_ContentPlaceHolder1_RepterDetails_ctl'
    stringTwo = '_HyperLink2'
    print(len(links))
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

def LoopForPages():
    page = True
    num = 2
    while(page):
        dic = GetLinkAndDate()
        for key in dic.keys():
            URL = dic[key]
            name = directory + NSD_Region +' ' + key + '.mp3' # Example Itanagar 03 Oct 2020.mp3
            #wget.download(URL,name)
            print('Donwloaded :',name)
            time.sleep(1) # make 15 while running .
        try:
          #ctl00_ContentPlaceHolder1_lbLast
          next = driver.find_element_by_link_text(str(num))
          next.click()
          print('[INFO] Next Page is found')
          num = num + 1
        except:
          print('[INFO] Next page is not found,quitting now')
          page = False
'---------------Performing the looping task---------------------'
directory ='/home/luvitusmaximus/Documents/ASR/Audio/'
PageInitialization()
LoopForPages()
driver.quit()
