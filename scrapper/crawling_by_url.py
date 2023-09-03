from selenium import webdriver
from bs4 import BeautifulSoup

class crawling_by_url:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def load_page(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)
        
    def extract_link(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup
        
    def close_driver(self):
        self.driver.quit()
        
    def run(self, link):
        self.load_page(link)
        soup = self.extract_link()
        # self.close_driver()
        return soup
