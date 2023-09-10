from datetime import datetime
from bs4 import BeautifulSoup  # 추가: BeautifulSoup 임포트
from scrapper.upload_images import upload_images  # 코드 예제에서 사용하지 않으므로 주석 처리

def nate_pann(soup, source_url):
    try:
        return_dict = {
            'site': 'https://pann.nate.com',
            'created_at': '',
            'source_url': source_url,
        }

        title_html = soup.find("div", {"class": "post-tit-info"})
        content_area = soup.find("div" , {"id": "contentArea"})
        # content_area에서 모든 img 태그를 찾습니다.
        scrapped_images = content_area.find_all("img")
        
        content_images = [];
        for image in scrapped_images:
            src = image.get('src', '')  # src 속성을 가져옵니다.
            alt = image.get('alt', '')  # alt 속성을 가져옵니다.
            content_images.append({'src': src, 'alt': alt})

        title = title_html.find("h1").text
        created_at = title_html.find("span", {"class": "date"}).text

        if not title:
            raise Exception('empty title')
        if not created_at:
            raise Exception('empty created_at')
        
        return_dict['title'] = title
        return_dict['images'] = upload_images(content_images, 'nate_paan');
        return_dict['created_at'] = datetime.strptime(created_at, '%Y.%m.%d %H:%M').isoformat()

        # upload_images 함수를 호출할 수 있는 부분입니다.
        # upload_images(image_url_dict, 'nate_paan')
        return return_dict

    except Exception as e:
        if str(e) == 'empty title':
            return 'empty title'
        if str(e) == 'empty created_at':
            return 'empty created_at'
        print('Catch the Exception:', e)
        return {}
