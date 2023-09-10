from datetime import datetime
from scrapper.upload_images import upload_images

def nate_pann(soup, source_url):
    try:
        return_dict = {
            'site': 'https://pann.nate.com',
            'created_at': '',
            'source_url': source_url  # 함수 인자로 전달
        }

        title_html = soup.find("div", {"class": "post-tit-info"})
        content_area = soup.find("div" , {"id": "contentArea"});
        title = title_html.find("h1").text

        created_at = title_html.find("span", {"class": "date"}).text
        if not title:
            raise Exception('empty title')
        if not created_at:
            raise Exception('empty created_at')
        

        return_dict['title'] = title
        return_dict['created_at'] = datetime.strptime(created_at, '%Y.%m.%d %H:%M').isoformat()
        
        print('content_area :::' , content_area);
        # image_url_dict=[];
        # upload_images(image_url_dict,'nate_paan')
        
        
        print('return_dict :::', return_dict)
        
        return return_dict

    except Exception as e:
        if str(e) == 'empty title':
            return 'empty title'
        if str(e) == 'empty created_at':
              return 'empty created_at'
        print('Catch the Exception ::: ',e)
        return {}
