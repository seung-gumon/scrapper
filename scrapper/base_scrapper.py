from datetime import datetime
import time
from bs4 import BeautifulSoup
import uuid
import hashlib
from scrapper.upload_images import upload_images
from scrapper.upload_images import upload_videos

class BaseScrapper:
    def __init__(self, site_name, site_url):
        self.site_name = site_name
        self.site_url = site_url

    def get_content_area(self, soup):
        raise NotImplementedError("SubClass 에서 상속받아서 Override 해야함")

    def get_title(self, soup):
        raise NotImplementedError("SubClass 에서 상속받아서 Override 해야함")

    def get_created_at(self, soup):
        raise NotImplementedError("SubClass 에서 상속받아서 Override 해야함")

    def scrap(self, soup, source_url):
        try:
            return_dict = {
                'site': self.site_url,
                'created_at': '',
                'source_url': source_url,
            }

            content_area = self.get_content_area(soup)
            title = self.get_title(soup)
            created_at = self.get_created_at(soup)
            
           
            # 날짜 형식을 처리하는 부분
            formats = ['%Y.%m.%d %H:%M:%S', '%Y.%m.%d %H:%M', '%Y.%m.%d (%H:%M:%S)']  # 추가된 형식
            parsed_datetime = None
            for fmt in formats:
                try:
                    parsed_datetime = datetime.strptime(created_at, fmt)
                    break
                except ValueError:
                    continue

            if parsed_datetime is None:
                raise ValueError(f'Unknown date format: {created_at}')

            
            if not title:
                raise Exception('empty title')
            if not created_at:
                raise Exception('empty created_at')
            

            scrapped_images = content_area.find_all("img")
            scrapped_videos = content_area.find_all("video")  # 오타 수정 (scrapped_vidoes -> scrapped_videos)

            # 이미지 처리
            content_images = []
            for image in scrapped_images:
                src = image.get('src', '')
                alt = image.get('alt', '')
                content_images.append({'src': src, 'alt': alt})

            # 비디오 처리
            content_videos = []
            for video in scrapped_videos:
                src = video.get('src', '')
                content_videos.append({'src': src})

            # 이미지와 비디오 모두 upload_images 함수를 사용하여 업로드
            convert_images = upload_images(content_images, self.site_name, source_url)
            for new_img, old_img in zip(convert_images, scrapped_images):
                old_img['src'] = new_img['src']

            convert_videos = upload_videos(content_videos, self.site_name, source_url)
            for new_vid, old_vid in zip(convert_videos, scrapped_videos):
                old_vid['src'] = new_vid['src']

            for a_tag in content_area.find_all('a'):
                a_tag.unwrap()
            for script_tag in content_area.find_all('script'):
                script_tag.decompose()

            updated_html_content = str(content_area).replace('\t', '').replace('\n', '').replace('\\', '')
            now = datetime.utcnow()
            # ID 생성
            uuid_str = str(uuid.uuid4())
            hash_object = hashlib.md5(uuid_str.encode())
            short_id = hash_object.hexdigest()[:8]  # 처음 8자리만 사용
            # ID 생성 끝
            return_dict['title'] = title
            return_dict['origin_created_at'] = parsed_datetime.isoformat()
            return_dict['created_at'] = now.isoformat() + "Z"
            return_dict['updated_at'] = now.isoformat() + "Z"
            return_dict['updated_html_content'] = updated_html_content
            return_dict['id'] = short_id


            return return_dict

        except Exception as e:
            if str(e) == 'empty title':
                return 'empty title'
            if str(e) == 'empty created_at':
                return 'empty created_at'
            print(f'Catch the Exception: {e}')
            return {}
