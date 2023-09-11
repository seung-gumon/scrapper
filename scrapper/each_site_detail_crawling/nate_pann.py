from datetime import datetime
from bs4 import BeautifulSoup
from scrapper.upload_images import upload_images
from scrapper.base_scrapper import BaseScrapper

class NatePannScrapper(BaseScrapper):
    def __init__(self):
        super().__init__('nate_paan', 'https://pann.nate.com')

    def get_content_area(self, soup):
        return soup.find("div", {"id": "contentArea"})

    def get_title(self, soup):
        return soup.find("div", {"class": "post-tit-info"}).find("h1").text

    def get_created_at(self, soup):
        return soup.find("div", {"class": "post-tit-info"}).find("span", {"class": "date"}).text