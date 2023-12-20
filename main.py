import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
import re

driver = webdriver.Chrome()
url = "https://www.forbes.com"


def filter_links(linklist):
    pattern = re.compile(r'^(?!forbes\.com)')
    filtered_links = [link['href'] for link in linklist if 'href' in link.attrs and pattern.match(link['href'])]
    return filtered_links

def scrape_links(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.text
        print(f'Title of the page: {title}')

        # Example: Find all links on the page
        links = soup.find_all('a', href=True)


        # print('\nLinks on the page:')
        # for link in links:
        #     print(link['href'])

        filtered_link_list=filter_links(links)
        for link in filtered_link_list:
            print(link['href'])

    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')

driver.get(url)
scrape_links(url)

print()