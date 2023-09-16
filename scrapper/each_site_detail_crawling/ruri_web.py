from datetime import datetime
from bs4 import BeautifulSoup
from scrapper.upload_images import upload_images
from scrapper.base_scrapper import BaseScrapper


class RuriWebScrapper(BaseScrapper):
      def __init__(self):
            super().__init__('ruri_web','https://bbs.ruliweb.com')
            
      def get_content_area(self, soup):
            return soup.find('div' , {'class' : "view_content autolink"})
      
      def get_title(self , soup):
            return soup.find("span" , {"class" : "subject_inner_text"}).text
      
      def get_created_at(self , soup):
            return soup.find("span" , {"class" : "regdate"}).text