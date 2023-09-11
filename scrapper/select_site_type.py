from .each_site_detail_crawling import fm_korea
from .each_site_detail_crawling import nate_pann
from .each_site_detail_crawling import dc_inside

def select_site(site_url):
      if site_url == 'https://www.fmkorea.com' :
            return fm_korea.fm_korea
      elif site_url == 'https://pann.nate.com' :
            return nate_pann.nate_pann
      elif site_url == 'https://gall.dcinside.com' :
            return dc_inside.dc_inside