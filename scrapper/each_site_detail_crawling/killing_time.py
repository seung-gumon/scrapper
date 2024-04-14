from scrapper.base_scrapper import BaseScrapper


class KillingTimeScrapper(BaseScrapper):
    def __init__(self):
        super().__init__('killing_time', 'https://www.killingtime.com')

    def get_content_area(self, soup):
        content_area = soup.find("div", {"class": "dable-content-wrapper"})
        if content_area:
            # Remove all 'code-block' elements within the content area
            code_blocks = content_area.find_all(class_="code-block")
            for block in code_blocks:
                block.decompose()
        return content_area

    def get_title(self, soup):
        return soup.find("h2", {"class": "single-post-title entry-title"}).text

    def get_created_at(self, soup):
        return soup.find("span", {"class": "meta-date"}).text