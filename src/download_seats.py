# Author: Jarome Leslie
# Seat counts downloader 

"""This script downloads tail number data from for Ohare Airport from the US Federal Aviation Administration

Usage: python download_seats.py
"""

import requests
from selenium import webdriver
import pandas as pd
import zipfile as zp
import glob
import os
import time



def download_seats():
    
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : os.getcwd()+ '/data/seats'}
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=311')

    
    targ_years= list(range(2013,2020,1))
    targ_years = list(map(str,targ_years))
    
    #STEP 1. LOCATE DOWNLOAD BUTTON
    download_bt = driver.find_element_by_xpath('//*[@id="content"]/table[1]/tbody/tr/td[2]/table[3]/tbody/tr/td[2]/button[1]')


    #STEP 2. SELECT FIELDS OF INTEREST (IGNORING DEFAULTS)

    # DEPARTURES SCHEDULED
    dep_sched_sel = driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[3]/td[1]/input').click()

    # DEPARTURES PERFORMED
    dep_perf_sel = driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[4]/td[1]/input').click()

    # SEATS
    seats_sel = driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[6]/td[1]/input').click()

    # PASSENGERS
    pass_sel = driver.find_element_by_xpath('/html/body/div[3]/div[3]/table[1]/tbody/tr/td[2]/table[4]/tbody/tr[7]/td[1]/input').click()

    
    #STEP 3. LOOP OVER YEARS OF INTEREST

    #FIND DROPDOWN FOR SELECTABLE YEARS 
    year_sel = driver.find_element_by_id("XYEAR")
    all_years = year_sel.find_elements_by_tag_name("option")


    #OUTER LOOP FOR EACH YEAR
    for year in all_years:
        if year.get_attribute("value") in targ_years:
            print("Value is: %s" % year.get_attribute("value"))
            year.click()


            #EXECUTE DOWNLOAD
            download_bt.click()
            time.sleep(5)
    

def merge_seats():
    entries = []

    
    zip_files = glob.glob('data/seats/*.zip')
    for zip_filename in zip_files:
        dir_name = os.path.splitext(zip_filename)[0]
        os.mkdir(dir_name)
        zip_handler = zp.ZipFile(zip_filename, "r")
        zip_handler.extractall(dir_name)

    # path = dir_name
    csv_files = glob.glob('data/seats/*/*.csv')

    entries =[]

    for csv in csv_files:
        entries.append(pd.read_csv(csv))
    
    combined_ord_seats = pd.concat(entries)
    combined_ord_seats.to_csv('data/ord_seats.csv')
    
    
def main():

     download_seats()
    merge_seats()
    

# script entry point
if __name__ == '__main__':
    main()    
