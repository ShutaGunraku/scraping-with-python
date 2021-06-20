"""
This file is a demonstration for scraping job information from indeed (https://www.indeed.com/).
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import requests
from selenium.webdriver.common.keys import Keys


global indeed_url
global indeed_ja_url
indeed_url = "https://www.indeed.com/"
indeed_ja_url = "https://jp.indeed.com/"

def scrape_indeed():
    # Configure settings for using driver
    options = webdriver.ChromeOptions()
    options.binary_location = "./bin/headless-chromium"
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('lang=en')
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    options.add_argument('--lang=en')
    driver = webdriver.Chrome('./bin/chromedriver', options=options)
    driver.get(indeed_ja_url)
    sleep(5)

    # Reached the destination
    driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[1]/div[1]/div/div[2]/input").send_keys("エンジニア")
    driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[2]/div[1]/div/div[2]/input").send_keys("東京")
    driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[3]/button").send_keys(Keys.ENTER)
    print(driver.title, "is the page.")
    print(driver.current_url, "is the current url")
    print(driver.page_source)

    # r = requests.get(driver.current_url)
    # print(r.content)

if __name__ == "__main__":
    scrape_indeed()