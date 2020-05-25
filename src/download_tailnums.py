# Author: Jarome Leslie
# Tail number downloader 

"""This script downloads tail number data from for Ohare Airport from the US Federal Aviation Administration

Usage: python download_tailnums.py
"""



import requests
from selenium import webdriver
import pandas as pd
import time

def extract_tail_info(tails):
    driver = webdriver.Chrome()
    result = {'tail_num': [], 'manufacturer': [], 'model': []}

    failures = {'tail_num': []}
    count =0
    driver = webdriver.Chrome()
    for tail in tails:
        time.sleep(5)
        try:
            tail = str(tail)
            url_ = 'https://registry.faa.gov/aircraftinquiry/NNum_Results.aspx?NNumbertxt='
            driver.get(url_+tail)            
            result['manufacturer'].append(driver.find_element_by_id("ctl00_content_lbMfrName").text)
            result['model'].append(driver.find_element_by_id("ctl00_content_Label7").text)
            result['tail_num'].append(tail)
            count += 1
            print(count)
        except:
            failures['tail_num'].append(tail)

    pd.DataFrame(result).to_csv('data/tailnums.csv')
    pd.DataFrame(failures).to_csv('data/missing_tailnums.csv')
    
    
    
def main():
    
    load_ord = pd.read_csv('data/ORD_OTP.csv')
    tail_nums = load_ord['TAIL_NUM'].unique()
    extract_tail_info(tail_nums)
    

# script entry point
if __name__ == '__main__':
    main()    