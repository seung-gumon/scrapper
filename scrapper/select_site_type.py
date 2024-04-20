from .each_site_detail_crawling import nate_pann
from .each_site_detail_crawling import dc_inside
from .each_site_detail_crawling import ruri_web
from .each_site_detail_crawling import bobae_dream
from .each_site_detail_crawling import killing_time
from .each_site_detail_crawling import dc_inside
from .each_site_detail_crawling import fm_korea



def select_site(site_url):
      if site_url == 'https://www.fmkorea.com' :
            fm_korea_instance = fm_korea.FmKoreaScrapper()
            return fm_korea_instance.scrap
      elif site_url == 'https://pann.nate.com' :
            nate_pann_instance = nate_pann.NatePannScrapper()
            return nate_pann_instance.scrap
      elif site_url == 'https://gall.dcinside.com' :
            dc_inside_instance = dc_inside.DCInsideScrapper()
            return dc_inside_instance.scrap
      elif site_url == 'https://bbs.ruliweb.com' :
            ruri_web_instance = ruri_web.RuriWebScrapper()
            return ruri_web_instance.scrap
      elif site_url == 'https://www.bobaedream.co.kr' :
            bobae_dream_instance = bobae_dream.BobaeDreamScrapper()
            return bobae_dream_instance.scrap
      elif site_url == 'https://killingtime.co.kr' :
            killing_time_instance = killing_time.KillingTimeScrapper()
            return killing_time_instance.scrap