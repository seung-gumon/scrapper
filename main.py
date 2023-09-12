from scrapper.extractor import link_extractor
from scrapper.crawling_by_url import crawling_by_url
from scrapper.select_site_type import select_site
from scrapper.upload_images import upload_images


site_url = "https://gall.dcinside.com"  # 해당줄은 Parameter로 삽입 예정

# 객체 생성 및 실행
extractor = link_extractor()
crawling = crawling_by_url()
transformed_json = extractor.run()



response_arr = []

def check_error(response_object):
    if isinstance(response_object, str):
        raise ValueError(response_object)
    if response_object == {}:
        raise KeyError("Dictionary is empty")


try:
    response_arr = []
    for site_object in transformed_json:
        if site_object['site_url'] == site_url:
            for link in site_object['links']:
                soup = crawling.run(link)
                selected_site_instance = select_site(site_url)
                response = selected_site_instance(soup,link)
                check_error(response)
                response_arr.append(response)
    print("Response Array ::: ",response_arr)
except (ValueError, KeyError) as e:
    if isinstance(e, ValueError):
        print(f"('{site_url} ::: {str(e)}')")
    if isinstance(e, KeyError):
        print(e)
        print(f"('{site_url} ::: 승석아 뭔가 잘못됐다. 확인해봐라..')")
    crawling.close_driver()

