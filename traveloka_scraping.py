# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:13:40 2020

@author: anandadwiarifian
"""


from csv import reader
import pandas as pd
import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

# CSV name and directory for export
directory_export = 'G:/My Drive/Documents in Drive/scraping/listing_traveloka_{0}.csv'.format(
    datetime.datetime.now().strftime("%d%m%Y"))

# City list CSV name and directory
directory_import = 'G:/My Drive/Documents in Drive/scraping/city_list.csv'

# define lists of hotel data
hotels = pd.DataFrame()
hotels['name'] = []
hotels['link'] = []
hotels['city'] = []
hotels['star'] = []
hotels['rating'] = []

# define the list of cities
unfound_cities = []

with open(directory_import, 'r') as read_obj:
    csv_reader = reader(read_obj)
    cities = list(csv_reader)


############################# start #########################
driver1 = webdriver.Chrome()
driver1.get('https://www.traveloka.com/')

for city in cities:  # loop per city

    assert "Hotel" in driver1.title
    page = 1

    # Type the next city name in search box
    elem = driver1.find_element_by_xpath("//input[@class='_3v6Dr _1nWNU']")

    elem.click()
    elem.clear()
    elem.send_keys(city+"  ")
    time.sleep(1)
    try:
        # Choose the first city option
        driver1.find_element_by_xpath(
            "//div[@class='_1XURZ']/descendant::div[contains(text(),'City')]").click()
    except NoSuchElementException:  # if not found
        try:
            # Choose the first area option
            driver1.find_element_by_xpath(
                "//div[@class='_1XURZ']/descendant::div[contains(text(),'Area')]").click()
        except NoSuchElementException:  # if both are not found, add the city name to the unfound city list
            unfound_cities.append(city)
            continue
    time.sleep(1)

    while True:  # loop per page
        print("Page: " + str(page))

        try:
            time.sleep(2)

            # get data
            hotels_per_page = pd.DataFrame()

            hotels_per_page['name'] = [i.text for i in driver1.find_elements_by_xpath(
                "//div[@class='_2HSF7 _2U03q _1Cnc5']/descendant::div[@class='_1z5je _10ZQX tvat-hotelName']")]
            hotels_per_page['type'] = [i.text for i in driver1.find_elements_by_xpath(
                "//div[@class='_2HSF7 _2U03q _1Cnc5']/descendant::div[@class='_3ohst Jewfo _2Vswb']")]
            hotels_per_page['star'] = [i.get_attribute("content") for i in driver1.find_elements_by_xpath(
                "//div[@class='_2HSF7 _2U03q _1Cnc5']/descendant::meta[@itemprop='ratingValue']")]
            hotels_per_page['city'] = [i.text for i in driver1.find_elements_by_xpath(
                "//div[@class='_2HSF7 _2U03q _1Cnc5']/descendant::div[@class='_3tICV']")]
            hotels_per_page['rating'] = [i.text for i in driver1.find_elements_by_xpath(
                "//div[@class='_2HSF7 _2U03q _1Cnc5']/descendant::span[@class='tvat-ratingScore']")]

        except StaleElementReferenceException:
            time.sleep(2)
            continue

        # save to dataframe
        hotels = pd.concat([hotels, hotels_per_page], ignore_index=True)

        # click the next page
        try:
            time.sleep(2)
            driver1.find_element_by_xpath("//div[@id='next-button']").click()
            page += 1
            continue
        except NoSuchElementException:
            break


hotels.drop_duplicates().reset_index(drop=True)
hotels.to_csv(directory_export, encoding='utf-8', index=False)
