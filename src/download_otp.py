# Author: Jarome Leslie
# On-Time Performance Data downloader
# Data taken from https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236
# Field descriptions provided https://www.transtats.bts.gov/Fields.asp?Table_ID=236

"""This script downloads weather data from for Ohare Airport from the US Bureau of Transportation

Usage: python download_otp.py
"""


import requests
from selenium import webdriver
import pandas as pd
import numpy as np
import zipfile as zp
from bs4 import BeautifulSoup
import time
import glob
import os



def download_otp(url, start_year, end_year):
#     path_parent = os.path.dirname(os.getcwd())
#     download_path = os.chdir(path_parent)
    # Instantiate browser
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : os.getcwd()+'/data/otp'}
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    
   
    #STEP 1. LOCATE DOWNLOAD BUTTON
    download_bt = driver.find_element_by_xpath('//*[@id="content"]/table[1]/tbody/tr/td[2]/table[3]/tbody/tr/td[2]/button[1]')

    
    #STEP 2. SELECT FIELDS OF INTEREST (IGNORING DEFAULTS)
    #DAY_OF_WEEK
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[7]/td[1]/input').click()
    
    #FLIGHT_DATE
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[8]/td[1]/input').click()

    #OP_UNIQUE_CARRIER
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[10]/td[1]/input').click()

    #TAIL_NUM
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[13]/td[1]/input').click()

    #FLIGHT_NUM
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[14]/td[1]/input').click()

    #ORIGIN
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[19]/td[1]/input').click()

    #DEST
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[29]/td[1]/input').click()

    #ARR_TIME
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[49]/td[1]/input').click()


    #ARR_DELAY
    driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[50]/td[1]/input').click()

    #STEP 3. LOOP OVER YEARS OF INTEREST

    #FIND DROPDOWN FOR SELECTABLE YEARS 
    year_sel = driver.find_element_by_id("XYEAR")
    all_years = year_sel.find_elements_by_tag_name("option")
    targ_years= list(range(start_year,end_year+1,1))
    
    month_sel = driver.find_element_by_id("FREQUENCY")
    all_months = month_sel.find_elements_by_tag_name("option")


    #OUTER LOOP FOR EACH YEAR
    for year in all_years:
        if int(year.get_attribute("value")) in targ_years:
            print(year.get_attribute("value"))
            year.click()
            
            for month in all_months:
                month.click()
                print(month.get_attribute("value"))


                #EXECUTE DOWNLOAD
                download_bt.click()
                time.sleep(15)
            

def aggregate_data(path):
    """
    Reads in data from downloaded zip files and writes a single aggregated csv file for ORD
    
    """
    entries = []

    zip_files = glob.glob(path+'/*.zip')
    for zip_filename in zip_files:
        with zp.ZipFile(zip_filename, "r") as myzip:
            dir_name = os.path.splitext(zip_filename)[0]
            os.mkdir(dir_name)
            zip_handler = zp.ZipFile(zip_filename, "r")
            zip_handler.extractall(dir_name)

    # path = dir_name
    csv_files = glob.glob(path+'/*/*.csv')

    for csv in csv_files:
        entries.append(pd.read_csv(csv).query('DEST == "ORD"'))
        


    combined_csvs = pd.concat(entries)
    combined_csvs.to_csv('data/ORD_OTP.csv')   
    
    
    
def main():
    
#     # Set month and year parameters
#     Months = list(range(1,13,1))
#     Months = list(map(str,Months))
#     targ_years= list(range(2013,2020,1))
#     targ_years = list(map(str,targ_years))
    
    TARGET = 'https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236'
    
    download_otp(TARGET, 2017, 2018)
    
    aggregate_data('data/otp')
    
    
# script entry point
if __name__ == '__main__':
    main()