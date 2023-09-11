from datetime import datetime
from bs4 import BeautifulSoup
from scrapper.upload_images import upload_images

def dc_inside(soup , source_url) :
      try:
            return_dict = {
                  'site': 'https://gall.dcinside.com',
                  'created_at': '',
                  'source_url': source_url,
            }
            
            content_area = soup.find("div", {"class": "writing_view_box"})
            
            title = soup.find("h3", {"class": "title ub-word"}).find("span", {"class": "title_subject"}).text
            created_at = soup.find("div", {"class": "gall_writer ub-writer"}).find("span", {"class": "gall_date"}).text
            
            if not title:
                  raise Exception('empty title')
            if not created_at:
                  raise Exception('empty created_at')
            
            
            scrapped_images = content_area.find_all("img")
            content_images = []
            
            for image in scrapped_images:
                  src = image.get('src', '')
                  alt = image.get('alt', '')
                  content_images.append({'src': src, 'alt': alt});
            
            convert_images = upload_images(content_images, 'dc_inside' , source_url)
            
            for new_img, old_img in zip(convert_images, scrapped_images):
                  old_img['src'] = new_img['src']
                  
        # a 태그만 제거, 내용은 남김
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
        print('최종 에러에 안잡혔음 확인 바람 :::', e)
        return {}