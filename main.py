from selenium import webdriver
from bs4 import BeautifulSoup


dc_inside_url = "https://gall.dcinside.com";
today_humor_url = "http://www.todayhumor.co.kr";
ruri_url = "https://bbs.ruliweb.com";
fm_korea = "https://www.fmkorea.com";
nate_pann = "https://pann.nate.com";
bobaeddream = "https://www.bobaedream.co.kr";
etoland = "http://www.etoland.co.kr";
# instiz = "https://www.instiz.net"


web_crawling_target = "https://todaybeststory.com/community.html"

comunity_links = [
    etoland,
    dc_inside_url,
    today_humor_url, 
    ruri_url, 
    fm_korea,
    nate_pann,
    bobaeddream
]



class LinkExtractor:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.collected_links = {}

    def load_page(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(5)

    def extract_links(self, limit):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        for comunity_link in comunity_links:
            links = soup.find_all('a', href=lambda x: x and x.startswith(comunity_link), limit=limit)
            self.collected_links[comunity_link] = []  # 이 커뮤니티에 대한 빈 리스트 초기화
            for link in links:
                href = link.get('href')
                self.collected_links[comunity_link].append(href)  # 이 커뮤니티에 대한 리스트에 추가


    def close_driver(self):
        self.driver.quit()

    def run(self,limit = 10):
        self.load_page(web_crawling_target)
        self.extract_links(limit)
        self.close_driver()

# 객체 생성 및 실행
extractor = LinkExtractor()
extractor.run()
# 추출한 링크 확인
print("Collected Links Length:", extractor.collected_links)