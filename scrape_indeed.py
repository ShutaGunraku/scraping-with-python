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
    # Enter "エンジニア" (Engineer) for the job category, and "東京" (Tokyo) for the location, then click enter.
    driver.find_element_by_xpath(
        "/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[1]/div[1]/div/div[2]/input").send_keys("エンジニア 在宅 簡単　インターン")
    driver.find_element_by_xpath(
        "/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[2]/div[1]/div/div[2]/input").send_keys("東京")
    driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[3]/button").send_keys(
        Keys.ENTER)
    print(driver.title, "is the page.")

    data_list = []
    page = 1
    print("the first page", page)
    print("url is", driver.current_url)
    while True:
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
            data = []
            # Get the job info by scraping with BeautifulSoup
            try: job_title = job_card.find("a", attrs={"class": "jobtitle"}).get("title").replace("\n", "")
            except: job_title = None
            try: company_name = job_card.find("span", attrs={"class": "company"}).text.replace("\n", "")
            except: company_name = None
            try: location = job_card.find("div", attrs={"class": "location"}).text.replace("\n", "")
            except: location = None
            try: income = job_card.find("span", attrs={"class": "salaryText"}).text.replace("\n", "")
            except: income = None
            try: job_type = job_card.find("div", attrs={"class": "jobTypeLabelsWrapper"}).text.replace("\n", "")
            except: job_type = None
            # print("company name:", company_name)
            # print("job title:", job_title)
            # print("location:", location)
            # print("income:", income)
            # print("job type:", job_type)
            data.append(company_name)
            data.append(job_title)
            data.append(location)
            data.append(income)
            data.append(job_type)
            data_list.append(data)
            # print(data_list)
            # break
        next_page = driver.find_element_by_class_name("pn")
        print("next page is", next_page.text)
        if next_page.text == "":
            break
        next_page.click()
        print("url is", driver.current_url)

    # Use pandas to get the job results table.
    df = pd.DataFrame(data_list)

    # Show all the columns
    pd.set_option("display.max_columns", None)

    df.columns = ["Company Name", "Job Title", "Location", "Income", "Job Type"]
    print(len(df))
    print(df)

    # r = requests.get(driver.current_url)
    # print(r.content)


if __name__ == "__main__":
    scrape_indeed()