"""
This file is a demonstration for scraping job information from indeed (https://www.indeed.com/).
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml

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
    sleep(1)

    # Reached the website.
    # Now enter "エンジニア" (Engineer) for the job category, and "東京" (Tokyo) for the location, then click enter.
    driver.find_element_by_xpath(
        "/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[1]/div[1]/div/div[2]/input").send_keys("エンジニア")
    driver.find_element_by_xpath(
        "/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[2]/div[1]/div/div[2]/input").send_keys("東京")
    driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[3]/button").send_keys(
        Keys.ENTER)
    print(driver.title, "is the page.")
    print(driver.current_url, "is the current url")
    # print(driver.page_source)

    # Use BeautifulSoup to scrape the website.
    res_url = driver.current_url
    raw_html = requests.get(res_url).text
    soup = BeautifulSoup(raw_html, "lxml")
    # print(soup.prettify())
    page_content = soup.find("table", attrs={"id": "pageContent"})
    # print(page_content)
    job_cards = page_content.find_all("div", attrs={"class": "jobsearch-SerpJobCard"})

    for job_card in job_cards:
        # print(job_card)

        # Get the job summary
        job_summary = job_card.find("a", attrs={"class": "jobtitle"}).get("title")
        # print(job_summary)
        job_desc = job_card.find("div", attrs={"class": "summary"})
        print(job_desc)

    # Use pandas to get the job results table.
    # dfs = pd.read_html(res_url)
    # print(len(dfs))
    # print(dfs)

    # r = requests.get(driver.current_url)
    # print(r.content)


if __name__ == "__main__":
    scrape_indeed()
