from datetime import datetime


def nate_pann(soup, source_url):
    try:
        return_dict = {
            'site': 'https://pann.nate.com',
            'created_at': '',
            'source_url': source_url  # 함수 인자로 전달
        }

        post_html = soup.find("div", {"class": "post-tit-info"})
        title = post_html.find("h1").text

        created_at = post_html.find("span", {"class": "date"}).text
        if not title:
            raise Exception('empty title')
        if not created_at:
            raise Exception('empty created_at')
        
        return_dict['title'] = title
        return_dict['created_at'] = datetime.strptime(created_at, '%Y.%m.%d %H:%M').isoformat()
        
        print('return_dict :::', return_dict)
        
        return return_dict

    except Exception as e:
        if str(e) == 'empty title':
            return 'empty title'
        if str(e) == 'empty created_at':
              return 'empty created_at'
        print('Catch the Exception ::: ',e)
        return {}