from extractor import site_names

class sort_community:
    def __init__(self, link_url):
        self.link_url = link_url

    def find_by_url(self):
        for key, value in site_names.items():
            if key in self.link_url:
                return {
                    "site_url": key,
                    "site_name": value,
                    "original_url": self.link_url
                }