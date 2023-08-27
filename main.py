from selenium import webdriver
from bs4 import BeautifulSoup


dc_inside_url = "https://gall.dcinside.com";
today_humor_url = "http://www.todayhumor.co.kr";
ruri_url = "https://bbs.ruliweb.com/";
fm_korea = "www.fmkorea.com";
nate_pann = "pann.nate.com";
bobaeddream = "https://www.bobaedream.co.kr";
instiz = "https://www.instiz.net/"



class LinkExtractor:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.collected_links = []

    def load_page(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    def extract_links(self,community_url , limit):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        links = soup.find_all('a', href=lambda x: x and x.startswith(community_url), limit=limit)
        for link in links:
            self.collected_links.append(link.get('href'))

    def close_driver(self):
        self.driver.quit()

    def run(self,community_url, limit = 10):
        self.load_page("https://todaybeststory.com/community.html")
        self.extract_links(community_url)
        self.close_driver()

# 객체 생성 및 실행
extractor = LinkExtractor()
extractor.run(dc_inside_url)
# 추출한 링크 확인
print("Collected Links Length:", extractor.collected_links)
print("Collected Links Length:", len(extractor.collected_links))
