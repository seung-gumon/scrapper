from selenium import webdriver
from bs4 import BeautifulSoup
import json
import psutil
from time import time, sleep
import os


# 웹사이트 URL과 이름 매핑
site_names = {
    "https://gall.dcinside.com": "디씨인사이드",
    "http://www.todayhumor.co.kr": "오늘의 유머",
    "https://bbs.ruliweb.com": "루리웹",
    "https://www.fmkorea.com": "FM Korea",
    "https://pann.nate.com": "네이트 판",
    "https://www.bobaedream.co.kr": "보배드림",
    "http://www.etoland.co.kr": "이토랜드",
}

# 나머지 코드는 동일
dc_inside_url = "https://gall.dcinside.com"
today_humor_url = "http://www.todayhumor.co.kr"
ruri_url = "https://bbs.ruliweb.com"
fm_korea = "https://www.fmkorea.com"
nate_pann = "https://pann.nate.com"
bobaeddream = "https://www.bobaedream.co.kr"
etoland = "http://www.etoland.co.kr"

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

def print_system_resources():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    process = psutil.Process(os.getpid())
    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {memory_info.percent}%")
    print(f"Process Memory Usage: {process.memory_info().rss / 1024 ** 2:.2f} MB")  # 현재 프로세스의 메모리 사용량 (MB 단위)


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
            self.collected_links[comunity_link] = []  
            for link in links:
                href = link.get('href')
                self.collected_links[comunity_link].append(href)  
    
    def close_driver(self):
        self.driver.quit()

    def transform_links_to_json(self):
        transformed_data = []
        for site_url, links in self.collected_links.items():
            site_name = site_names.get(site_url, "Unknown site")
            transformed_data.append({
                "site_url": site_url,
                "site_name": site_name,
                "links": links
            })
        return json.dumps(transformed_data, indent=2, ensure_ascii=False)

    def run(self, limit=10):
        self.load_page(web_crawling_target)
        self.extract_links(limit)
        self.close_driver()
        return self.transform_links_to_json()


def main():
    print("===== Before running the program =====")
    print_system_resources()

    start_time = time()
    
    # 객체 생성 및 실행
    extractor = LinkExtractor()
    transformed_json = extractor.run()


    end_time = time()
    
    print("===== After running the program =====")
    print_system_resources()
    print(f"Time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()
