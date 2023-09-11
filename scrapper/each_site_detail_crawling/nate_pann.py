from datetime import datetime
from bs4 import BeautifulSoup
from scrapper.upload_images import upload_images

def nate_pann(soup, source_url):
    try:
        return_dict = {
            'site': 'https://pann.nate.com',
            'created_at': '',
            'source_url': source_url,
        }

        title_created_wrapper_html = soup.find("div", {"class": "post-tit-info"})
        content_area = soup.find("div", {"id": "contentArea"})

        title = title_created_wrapper_html.find("h1").text
        created_at = title_created_wrapper_html.find("span", {"class": "date"}).text        

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

        convert_images = upload_images(content_images, 'nate_paan', source_url)

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
        print('Catch the Exception:', e)
        return {}
