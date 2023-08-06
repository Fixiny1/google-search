import time

import requests as r
from bs4 import BeautifulSoup as bs
from pyairtable import Table
from random import choice
from time import sleep

# VAR
API_ID = 'key2ZcQQphsmRO8RI'
BASE_ID = 'app56B7PnK9ecp8Qb'
NAME_TABBLE = 'tblh8H2ePB926Lkpo'
DOMEN_NAME = "domen"
SEARCH_NAME = "Search"
RESULT_NAME = "order"
SELECT_NAME = "Select"

# User-data
_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]

# Search Algoritm
def getPositionGoogle(search, domen, max_page=2):
    page_index = 0
    while page_index <= max_page:
        page = r.get(f"https://www.google.com/search?q={search}&start={page_index * 10}", headers={"User-Agent": choice(_useragent_list)})
        soup = bs(page.content, 'html.parser')
        result_blocks = soup.find_all('div', class_="g")
        result_link = []
        for result_block in result_blocks:
            link = result_block.find('a', href=True)['href']
            if link not in result_link and link[0] not in ['#', '/']:
                result_link.append(link)

        print(result_link)

        for index, link in enumerate(result_link):
            if domen in link:
                return (index + 1) + (page_index * 10)
        page_index += 1
        sleep(2)
    return -1

# Main Program
if __name__ == '__main__':
    table = Table(API_ID, BASE_ID, NAME_TABBLE)
    while True:
        for field in table.all(formula="IF({"+SELECT_NAME+"}='Update Now', 1, 0)"):
            id = field['id']
            Search = field['fields'][SEARCH_NAME]
            domen = field['fields'][DOMEN_NAME]
            table.update(id, {RESULT_NAME: getPositionGoogle(Search, domen), SELECT_NAME: 'Update'})
            time.sleep(60)
    print('Complete')