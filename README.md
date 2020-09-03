# WebScraping-for-Audio-Transcript-download
This repository contains the python files used to download the Audio-Transcript files from the newsonair.com website using selenium and chrome websriver.

# Automation of Audio-Transcript download from newsonair.com

This script automates the process of downloading the audio transcript for the news files availabe on [newsonair.com](http://newsonair.com/RNU-NSD-Audio-Archive-Search.aspx) ,using the selenium python package and the chrome webdriver. All the dependencies are listed with instructions to use to run the script WebScraping_NSD.py.

# Dependencies
THe following are the requirements to run the WebScraping_NSD.py, all the files and instructions are written for Windows 10 PC.
  
  - Chrome web browser, v85 click[ here.](http://newsonair.com/RNU-NSD-Audio-Archive-Search.aspx)
  - ChromeWebDriver, click [here.](https://chromedriver.chromium.org/downloads)
  - Selenium Python package. (See installation section)

### Selenium package install
To install the selenium python package from the terminal,run the following command:
```sh
$ pip install -U selenium
```
Alternately, you can download the source distribution from [PyPI](https://pypi.org/project/selenium/#files) (e.g. selenium-3.141.0.tar.gz), unarchive it, and run:
```sh
$ python setup.py install
```
### Excecuting the script
The script contains some environment path variables that you must change in order to avoid driver exceptions, The changes that are to be made are as follows:
 
 - On line 15, the path to donwload the files should be changed as follows.
```python
ChromeOptions.add_experimental_option("prefs",{"download.default_directory":"DIRECOTRY TO DOWNLOAD"})
```   
 - On line 16 the path to the chrome driver should be changed to where you have extracted the chromedriver.
```python
driver = webdriver.Chrome(executable_path='PATH TO CHROMEDRIVER.EXE',chrome_options=ChromeOptions)
```   
After excecuting the changes , we can run the script to download all the pdf files to the respective directory.
