from .extractor import site_names



resultArray = []

class SortCommunity:
    def __init__(self, link_url):
        self.link_url = link_url

    def find_by_url(self):
        for key, value in site_names.items():

            if key in self.link_url:
                obj = {
                    "site_url": key,
                    "site_name": value,
                    "original_url": self.link_url
                }
                return obj


def separate_community(link_urls):
    for link_url in link_urls:
        sort_community_instance = SortCommunity(link_url)
        result = sort_community_instance.find_by_url()
        if result is not None:
            resultArray.append(result)
    return resultArray


