from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json  # JSON 처리를 위한 모듈 추가

# 기존에 실행 중인 Chrome에 연결
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)

# 열려있는 모든 탭의 핸들을 가져오기
window_handles = driver.window_handles

link_arr = []
for handle in window_handles:
    # 탭으로 전환
    driver.switch_to.window(handle)
    # 현재 탭에서의 URL 출력 (또는 다른 크롤링 작업 수행)
    link_arr.append(driver.current_url)

# 리스트를 JSON 형태로 변환
json_str = json.dumps(link_arr, indent=4)

# JSON 문자열을 파일에 저장
with open('scrapping_target_links.json', 'w') as f:
    f.write(json_str)
