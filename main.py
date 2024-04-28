from scrapper.extractor import link_extractor
from scrapper.crawling_by_url import crawling_by_url
from scrapper.select_site_type import select_site
from scrapper.sort_community import separate_community
from scrapper.string_html_extract import string_html_extract
from scrapper.save_post_data import save_post_data


import json



# 파일에서 JSON 데이터 읽기
with open('scrapping_target_links.json', 'r') as f:
    scrapping_target_link_arr = json.load(f)



# site_url = "https://gall.dcinside.com"  # 해당줄은 Parameter로 삽입 예정
# site_url = "https://www.bobaedream.co.kr"


# 객체 생성 및 실행
crawling = crawling_by_url()



transformed_json = separate_community(scrapping_target_link_arr)


print("Transformed_json :::" , transformed_json)

def check_error(response_object):
    if isinstance(response_object, str):
        raise ValueError(response_object)
    if response_object == {}:
        raise KeyError("Dictionary is empty")


try:
    response_arr = []
    for site_object in transformed_json:
                soup = crawling.run(site_object["original_url"])
                selected_site_instance = select_site(site_object["site_url"])
                response = selected_site_instance(soup , site_object["original_url"])
                check_error(response)
                response_arr.append(response)
    print("Response_arr :::" , response_arr)
    save_post_data(response_arr)
except (ValueError, KeyError) as e:
    if isinstance(e, ValueError):
        print(e)
        # print(f"('{site_url} ::: {str(e)}')")
    if isinstance(e, KeyError):
        print(e)
    crawling.close_driver()
