from datetime import datetime
from bs4 import BeautifulSoup
from scrapper.upload_images import upload_images
from scrapper.base_scrapper import BaseScrapper
import re  # 정규 표현식 라이브러리


class BobaeDreamScrapper(BaseScrapper):
    def __init__(self):
        super().__init__('bobae_dream', 'https://www.bobaedream.co.kr')

    def get_content_area(self, soup):
        return soup.find("div", {"class": "bodyCont"})

    def get_title(self, soup):
        return soup.find("div", {"class": "writerProfile"}).find("dt")['title']

    def get_created_at(self, soup):
      count_group = soup.find("span", {"class": "countGroup"})
      if count_group:
            last_text = list(count_group.stripped_strings)[-1]
            return re.sub(r'\([^)]*\)', '', last_text).strip()