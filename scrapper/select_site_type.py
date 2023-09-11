from .each_site_detail_crawling import fm_korea
from .each_site_detail_crawling import nate_pann
from .each_site_detail_crawling import dc_inside

def select_site(site_url):
      if site_url == 'https://www.fmkorea.com' :
            return fm_korea.fm_korea
      elif site_url == 'https://pann.nate.com' :
            nate_pann_instance = nate_pann.NatePannScrapper()
            return nate_pann_instance.scrap
      elif site_url == 'https://gall.dcinside.com' :
            dc_inside_instance = dc_inside.DCInsideScrapper()
            return dc_inside_instance.scrap