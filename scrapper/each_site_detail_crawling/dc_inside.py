from datetime import datetime
from bs4 import BeautifulSoup
from scrapper.upload_images import upload_images
from scrapper.base_scrapper import BaseScrapper

class DCInsideScrapper(BaseScrapper):
    def __init__(self):
        super().__init__('dc_inside', 'https://gall.dcinside.com')

    def get_content_area(self, soup):
        return soup.find("div", {"class": "writing_view_box"})

    def get_title(self, soup):
        return soup.find("h3", {"class": "title ub-word"}).find("span", {"class": "title_subject"}).text

    def get_created_at(self, soup):
        return soup.find("div", {"class": "gall_writer ub-writer"}).find("span", {"class": "gall_date"}).text