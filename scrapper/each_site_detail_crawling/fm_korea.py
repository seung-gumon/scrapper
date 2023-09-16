from datetime import datetime
from bs4 import BeautifulSoup
from scrapper.upload_images import upload_images
from scrapper.base_scrapper import BaseScrapper

class FmKoreaScrapper(BaseScrapper):
  def __init__(self):
    super().__init__('fm_korea','https://www.fmkorea.com')
    
  def get_content_area(self, soup):
    return soup.find('div' , {'class' : "xe_content"})
  
  def get_title(self , soup):
    return soup.find("span" , {"class" : "np_18px_span"}).text
  
  def get_created_at(self , soup):
    return soup.find("span" , {"class" : "date m_no"}).text