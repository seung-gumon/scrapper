from datetime import datetime
from bs4 import BeautifulSoup
from scrapper.upload_images import upload_images

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
            
            if not title:
                raise Exception('empty title')
            if not created_at:
                raise Exception('empty created_at')

            scrapped_images = content_area.find_all("img")
            content_images = []

            for image in scrapped_images:
                src = image.get('src', '')
                alt = image.get('alt', '')
                content_images.append({'src': src, 'alt': alt})

            convert_images = upload_images(content_images, self.site_name, source_url)

            for new_img, old_img in zip(convert_images, scrapped_images):
                old_img['src'] = new_img['src']

            for a_tag in content_area.find_all('a'):
                a_tag.unwrap()

            updated_html_content = str(content_area).replace('\t', '').replace('\n', '').replace('\\', '')

            return_dict['title'] = title
            return_dict['created_at'] = datetime.strptime(created_at, '%Y.%m.%d %H:%M').isoformat()
            return_dict['updated_html_content'] = updated_html_content
            return return_dict

        except Exception as e:
            if str(e) == 'empty title':
                return 'empty title'
            if str(e) == 'empty created_at':
                return 'empty created_at'
            print(f'Catch the Exception: {e}')
            return {}
