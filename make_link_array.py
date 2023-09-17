from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 1. MAC OS일 경우 아래의 명령어를 터미널에 입력하여 크롬을 실행합니다.
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
# 2. Chrome으로 실행시킨 브라우저에서 필요한 사이트에 들어간 후 , vs code 에서 'python3 make_link_array.py' 를 실행합니다.


# 기존에 실행 중인 Chrome에 연결
chrome_options = Options()
print('chrome Options :::' , chrome_options);
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)
print("Driver :::" , driver);

# 열려있는 모든 탭의 핸들을 가져오기
window_handles = driver.window_handles

link_arr = []
for handle in window_handles:
    # 탭으로 전환
    driver.switch_to.window(handle)
    # 현재 탭에서의 URL 출력 (또는 다른 크롤링 작업 수행)
    link_arr.append(driver.current_url)
    # 이곳에서 원하는 크롤링 로직을 추가할 수 있습니다.
print('현재 크롤링 하려고 켜둔 인터넷 창' , link_arr);