from scrapper.base_scrapper import BaseScrapper
import re

class KillingTimeScrapper(BaseScrapper):
    def __init__(self):
        try:
            super().__init__('killing_time', 'https://www.killingtime.com')
        except Exception as e:
            print(f"Error in __init__: {e}")

    def get_content_area(self, soup):
        try:
            content_area = soup.find("div", {"class": "dable-content-wrapper"})
            if content_area:
                code_blocks = content_area.find_all(class_="code-block")
                for block in code_blocks:
                    block.decompose()
            return content_area
        except Exception as e:
            print(f"Error in get_content_area: {e}")
            return None

    def get_title(self, soup):
        try:
            title_element = soup.find("h2", {"class": "single-post-title entry-title"})
            if title_element:
                return title_element.text
            return None
        except Exception as e:
            print(f"Error in get_title: {e}")
            return None

    def get_created_at(self, soup):
        try:
            created_at_element = soup.find("li", {"class": "meta-date"})
            if created_at_element:
                # 정규 표현식을 사용하여 날짜 부분만 추출합니다.
                date_text = re.search(r'\d{4}년 \d{1,2}월 \d{1,2}일', created_at_element.text)
                if date_text:
                    return date_text.group()
            return None
        except Exception as e:
            print(f"Error in get_created_at: {e}")
            return None
