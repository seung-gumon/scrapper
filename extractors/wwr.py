from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(word):
      base_url = "https://weworkremotely.com/remote-jobs/search?term="
      response = get(f"{base_url}{word}")
      if response.status_code != 200:
            print("웹사이트 정보를 가져올 수 없습니다.")
      else:
            resuls = []
            soup = BeautifulSoup(response.text, "html.parser")
            jobs = soup.find_all("li", {"class": "feature"})
            for job in jobs:
                  title = job.find("span", {"class": "title"}).string
                  company = job.find("span", {"class": "company"}).string
                  link = job.find("a")["href"]
                  resuls.append({"title": title, "company": company, "link": f"https://weworkremotely.com{link}"})
            return resuls