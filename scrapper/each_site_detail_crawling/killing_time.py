from scrapper.base_scrapper import BaseScrapper
import re

class KillingTimeScrapper(BaseScrapper):
    def __init__(self):
        try:
            super().__init__('killing_time', 'https://www.killingtime.com')
        except Exception as e:
            print(f"Error in __init__: {e}")
            
    def clean_attributes(self, soup):
        for tag in soup.find_all(True):
            if tag.name == 'figure':  # figure 태그를 div 태그로 변경합니다.
                tag.name = 'div'
            # 유지할 속성을 정의합니다.
            allowed_attrs = {'href', 'src'}
            attrs = dict(tag.attrs)
            for attr in attrs:
                if attr not in allowed_attrs:
                    del tag.attrs[attr]
        return soup

    def get_content_area(self, soup):
        try:
            content_area = soup.find("div", {"class": "dable-content-wrapper"})
            if content_area:
                code_blocks = content_area.find_all(class_="code-block")
                for block in code_blocks:
                    block.decompose()
                    
                # 필요한 속성을 제거하고 figure 태그를 div로 변환합니다.
                content_area = self.clean_attributes(content_area)

                # 불필요한 속성을 제거합니다.
                del content_area['class']
                del content_area['itemprop']
            print("Content Area :::", content_area)
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
