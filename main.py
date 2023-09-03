from scrapper.extractor import link_extractor
from scrapper.crawling_by_url import crawling_by_url
from bs4 import BeautifulSoup
from scrapper.site.fm_korea import fm_korea


site_url = "https://www.fmkorea.com";

# 객체 생성 및 실행
extractor = link_extractor()
crawling = crawling_by_url()
transformed_json = extractor.run()




for site_object in transformed_json:
    if site_object['site_url'] == site_url:
          for link in site_object['links']:
            soup = crawling.run(link);
            response = fm_korea(soup)