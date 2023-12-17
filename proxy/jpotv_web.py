import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

'''
spotv : 9
spotv2 : 10
spotv prime : 15
spotv golf : 11
spotv on : 1
spotv on 2 : 2
nba tv : 3
'''
CHANNEL_LIST = ["9", "10", "15", "11", "1", "2", "3"]

def close_all_popups(browser):
    time.sleep(2)
    try:
        # close button find
        button = browser.find_elements(By.ID, "Close")
        
        # 'close'이라는 단어가 포함된 id를 가진 이미지 찾아 클릭
        for image in button:
            image_id = image.get_attribute("id")
            if "Close" in image_id:
                image.click()
    except:
        print("There's no pop up")
    
    time.sleep(2)

# mitmproxy가 실행되는 호스트와 포트
proxy = "localhost:18080"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server={proxy}")

# SNS 로그인 정보
EMAIL = "gate_flowers@naver.com"
PASSWORD = "arch0115"

capabilities = webdriver.DesiredCapabilities.CHROME.copy()
capabilities["acceptInsecureCerts"] = True

service = Service(ChromeDriverManager().install())
chromedriver_version = "114.0.5735.16"
browser = webdriver.Chrome(service=service, options=chrome_options)

browser.maximize_window()
home_url = "https://www.spotvnow.co.kr/"
browser.get(home_url)
time.sleep(2)

# 이메일, 비밀번호 입력
email_input = browser.find_element(By.CSS_SELECTOR,
    "input.login_input[type='email']"
)  # 이메일 입력 필드 선택자 수정
email_input.send_keys(EMAIL)

password_input = browser.find_element(By.CSS_SELECTOR,
    "input.login_input[type='password']"
)  # 이메일 입력 필드 선택자 수정
password_input.send_keys(PASSWORD)

# 로그인 버튼 클릭
login_button = browser.find_element(By.CSS_SELECTOR,
    "button.default.ok.active"
)  # 로그인 버튼 선택자 수정
login_button.click()

close_all_popups(browser)

# go to tv channel
tv_channel_li = browser.find_element(By.CSS_SELECTOR, "li.header-ch")
tv_channel_li.click()
time.sleep(2)
div_element = browser.find_element(By.CSS_SELECTOR, "div.Program-Channel")
div_element.click()
time.sleep(5)

# #find key part
# cookies = {}
# cookies = browser.get_cookies()
# try: 
#     for cookie in cookies:
#         if cookie['name'] == 'CloudFront-Key-Pair-Id':
#             key_pair = cookie['value']
#         if cookie['name'] == 'CloudFront-Policy':
#             policy = cookie['value']
#         if cookie['name'] == 'CloudFront-Signature':
#             sig = cookie['value']
# except:
#     "cookies something wrong. check need"
urls = []
#new_string = f"chunklist_b9192000.m3u8?Policy={policy}&Signature={sig}&Key-Pair-Id={key_pair}"    

# 파일 삭제
with open(f'../result/output.txt', 'w') as file:
    pass

for i in CHANNEL_LIST:
    url = f"https://www.spotvnow.co.kr/player?type=channel&id={i}"
    browser.get(url)
    time.sleep(5)

# #extra channel
# for i in range(1, 10):
#     url=f'https://ch0{i}-livescdn.spotvnow.co.kr/ch0{i}/spt0{i}_pc.smil/{new_string}'
#     browser.get(url)
#     time.sleep(3)

# #extra channel 2
# for i in range(10,31):
#     url=f'https://ch{i}-livescdn.spotvnow.co.kr/ch{i}/spt{i}_pc.smil/{new_string}'
#     browser.get(url)
#     time.sleep(3)

#for highlights
# browser.get(home_url)
# time.sleep(2)

# highlight_elements_xpaths = []
# elements = browser.find_elements(By.LINK_TEXT, "//*[contains(text(), '하이라이트')]")
# for element in elements:
#     # 각 요소에 대한 XPath를 리스트에 추가
#     highlight_elements_xpaths.append(browser.execute_script(
        # "return generateXPath(arguments[0]);", element))

# # XPath를 사용하여 각 요소에 접근하고 클릭
# for xpath in highlight_elements_xpaths:
#     try:
#         # 원래 URL로 돌아가기
#         browser.get(home_url)

#         # XPath를 사용하여 요소 찾기
#         element_to_click = browser.find_element(By.XPATH, xpath)
        
#         # 요소 클릭
#         element_to_click.click()

#         time.sleep(3)

#     except:
#         print("can't find highlights")


filename = '../result/output.txt'

# # 파일에서 내용 읽기
# with open(filename, 'r') as file:
#     lines = file.readlines()

# # 각 줄을 처리
# modified_lines = []
# for line in lines:
#     parts = line.strip().split('/')
#     if parts:
#         parts.pop()
#     parts.append(new_string)
#     modified_line = '/'.join(parts)
#     modified_lines.append(modified_line + '\n')

# # 수정된 내용으로 파일에 다시 쓰기
# with open(filename, 'w') as file:
#    file.writelines(modified_lines)


browser.quit()


# 접속해서 팝업 끄기,
# 팝업 끄고 나면 채널 누르기 
# 첫 채널 들어가서 키 따기
# 아웃풋 json으로