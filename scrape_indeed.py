"""
This file is a demonstration for scraping job information from indeed (https://jp.indeed.com/).
"""
__author__ = "Shuta Gunraku"

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd

global indeed_ja_url
indeed_ja_url = "https://jp.indeed.com/"


def scrape_indeed(job, location):
    """
    This function will visit the website of indeed, and search the site for job offers
    using parameters for the search condition.
    :param job: The job category with which the search will be looking for jobs.
    :param location: The location within which the search will be conducted.
    """
    print("Scraping Initiated.")

    # Configure settings for using driver
    options = webdriver.ChromeOptions()
    options.binary_location = "./bin/headless-chromium"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('./bin/chromedriver', options=options)
    driver.get(indeed_ja_url)
    sleep(2)

    # Reached the website.
    try:
        # Enter the 'job' for the job category
        driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[1]/div[1]/div/div[2]/input").send_keys(job)
        sleep(2)
        # Enter the 'location' for the location
        driver.find_element_by_xpath(
            "/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[2]/div[1]/div/div[2]/input").send_keys(location)
        sleep(2)
        # Click enter
        driver.find_element_by_xpath("/html/body/div/div[2]/div[3]/div[1]/div/div/div/form/div[3]/button").send_keys(
            Keys.ENTER)
        sleep(5)

        # Scrape the job info and store it in data_list[]
        data_list = []
        page_number = 0
        while True:
            page_number += 1
            # Use BeautifulSoup to scrape the website.
            res_url = driver.current_url
            raw_html = requests.get(res_url).text
            soup = BeautifulSoup(raw_html, "lxml")
            page_content = soup.find("table", attrs={"id": "pageContent"})
            job_cards = page_content.find_all("div", attrs={"class": "jobsearch-SerpJobCard"})

            # Get elements of each job offer, remove indentations then add them to data_list[]
            for job_card in job_cards:
                # Get the job info by scraping with BeautifulSoup
                data = []
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

            # Try to click the next page link.
            try:
                page_button = driver.find_element_by_xpath(f"//span[@class='pn' and text()='{str(page_number + 1)}']")
                page_button.click()
                driver.get(driver.current_url)
                sleep(2)

            except:
                print("Exiting.")
                break

    # Need to avoid recaptcha thus terminate execution.
    except:
        pass

    # Use pandas to get the job results table.
    df = pd.DataFrame(data_list)
    # Show all the columns
    pd.set_option("display.max_columns", None)
    # Add column names
    df.columns = ["Company Name", "Job Title", "Location", "Income", "Job Type"]
    df.sort_values(by=["Company Name"])
    # Output the data to a csv file
    df.to_csv('indeed_engineer_jobs.csv', encoding='utf-8')


if __name__ == "__main__":
    scrape_indeed("エンジニア 在宅　インターン", "東京都 府中市")