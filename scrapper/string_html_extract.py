from bs4 import BeautifulSoup

official_attributes = {
    'img': ['src'],
    'video': ['src'],
    'div': [],
    'p': [],
    'span': [],
}


def string_html_extract(response_arr):
    for item in response_arr:
        soup = BeautifulSoup(item.get('updated_html_content', ''), 'html.parser')

        content = []

        for tag_name, attributes in official_attributes.items():
            for tag in soup.find_all(tag_name):
                tag_data = {"tag": tag_name}

                # div, p, span 태그의 경우 텍스트를 추출
                if tag_name in ['div', 'p', 'span']:
                    text = tag.get_text(strip=True)
                    if text:
                        tag_data["text"] = text

                # img, video 태그의 경우 속성을 추출
                for attr in attributes:
                    if tag.has_attr(attr):
                        tag_data[attr] = tag[attr]

                content.append(tag_data)

        # updated_html_content 제거 및 content 추가
        if 'updated_html_content' in item:
            del item['updated_html_content']
        item['contents'] = content

    return response_arr