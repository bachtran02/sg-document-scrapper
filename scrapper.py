import re
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup


class ScrapeData:
    def __init__(self, committee, year):
        self.committee = committee
        self.year = year
        load_dotenv()

    @staticmethod
    def editString(string):
        return re.sub(' +', ' ', re.sub('\n', ' ', string.replace("DASB", "DASG")))

    def scrape(self):
        response = ""
        data = dict()
        usable_tag = ["h2", "h3"]
        request_url = f'{os.environ.get("REQUEST_URL_HEADER")}{self.committee}/agendasminutes/{self.year}.html'
        try:
            response = requests.get(request_url)
        except requests.exceptions.RequestException as e:
            # print(e)
            exit()

        soup = BeautifulSoup(response.text, "html.parser")
        main_data = soup.find('div', {"class": "col-xs-12 col-lg-9 l-content pull-right full-width"})
        all_ul = main_data.find_all('ul')

        for ul in all_ul:
            prev_e = ul.find_previous_sibling()

            if prev_e is None or prev_e.name not in usable_tag:
                continue

            header = prev_e.text
            item_list = []
            e_list = ul.find_all("a", href=True)
            for e in e_list:
                # print(e.text, url_header + e['href'])
                item_list.append({"title": self.editString(e.text), "link": os.environ.get('URL_HEADER') + e['href']})
            data[header] = item_list

        return data
