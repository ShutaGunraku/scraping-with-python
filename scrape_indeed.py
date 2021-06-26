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

global indeed_ja_url
indeed_ja_url = "https://jp.indeed.com/"


def scrape_indeed(job, location):
    # Configure settings for using driver
    options = webdriver.ChromeOptions()
    options.binary_location = "./bin/headless-chromium"
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('./bin/chromedriver', options=options)
    driver.get(indeed_ja_url)
    sleep(1)

    # Reached the website.
    # Enter 'job' for the job category, and 'location' for the location, then click enter.
    driver.find_element_by_xpath(
        "/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[1]/div[1]/div/div[2]/input").send_keys(job)
    driver.find_element_by_xpath(
        "/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[2]/div[1]/div/div[2]/input").send_keys(location)
    driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[3]/button").send_keys(
        Keys.ENTER)
    print(driver.title, "is the page.")

    # Scrape the job info and store in data_list[]
    data_list = []
    page = 1
    print("the first page", page)
    print("url is", driver.current_url)

    page_number = 0
    while True:
        page_number += 1
        # Use BeautifulSoup to scrape the website.
        res_url = driver.current_url
        raw_html = requests.get(res_url).text
        soup = BeautifulSoup(raw_html, "lxml")
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
            data.append(company_name)
            data.append(job_title)
            data.append(location)
            data.append(income)
            data.append(job_type)
            data_list.append(data)

        try:
            page_button = driver.find_element_by_xpath(f"//span[@class='pn' and text()='{str(page_number + 1)}']")
            print("The page button", page_button.text)
            page_button.click()
            print("url is", driver.current_url)
            driver.get(driver.current_url)
        except:
            print("Exiting")
            break

        # page_buttons = driver.find_elements_by_class_name("pn")
        # print(driver.current_url)
        # condition = False
        # for pn in page_buttons:
        #     try:
        #         if pn.text == str(page_number + 1):
        #             print("the next page is", pn.text)
        #             pn.click()
        #             print("url is", driver.current_url)
        #             driver.get(driver.current_url)
        #             condition = True
        #     except:
        #         continue
        #
        # if not condition:
        #     print("exiting")
        #     break

    # Use pandas to get the job results table.
    df = pd.DataFrame(data_list)
    # Show all the columns
    pd.set_option("display.max_columns", None)
    # Add column names
    df.columns = ["Company Name", "Job Title", "Location", "Income", "Job Type"]
    print(df)
    # Output the data to a csv file
    df.to_csv('indeed_engineer_jobs.csv', encoding='utf-8')


if __name__ == "__main__":
    scrape_indeed("エンジニア 在宅　簡単　週4 未経験　サポート", "東京都 府中市")