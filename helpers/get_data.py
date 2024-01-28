import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)


from lib.postgre_connection import PostgreeDatabase
import requests
from bs4 import BeautifulSoup
import logging



MAIN_URL = "https://www.dicio.com.br/palavras-mais-buscadas"
NUMBER_OF_PAGES = 50 # From 1 to 50 

logging.basicConfig(level=logging.INFO)

def get_db_connection():
    try:
        return PostgreeDatabase()
    except Exception as exception:
        raise Exception("Could not connect with the database") from exception

if __name__ == "__main__":
    words = set()

    with get_db_connection() as conn:    
        for page_number in range(1, NUMBER_OF_PAGES + 1):
            logging.info(f"Colleting data from page {page_number}")

            the_page = requests.get(f"{MAIN_URL}/{page_number}", headers={"User-Agent":"Mozilla/5.0"})
            if (the_page.status_code != 200):
                logging.warning(f"Was not possible to get the data from page {page_number}")
                continue

            soup = BeautifulSoup(the_page.text, 'lxml')
            words_list = soup.find(class_='list')
            words_items = words_list.find_all('a')
            for word in words_items:
                the_word = word.contents[0].strip()
                words.add(the_word)

        logging.info("Inserting data to db")
        for idx, word in enumerate(words):
            logging.info(f"[{idx+1}/{len(words)}]")
            conn.insert(word)
