import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
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
    try:
        all_popups = browser.find_elements_by_css_selector("label[id='Close']")
        for popup in all_popups:
            popup.click()
            print("Popup closed.")
    except NoSuchElementException:
        print("No such element.")
    except ElementNotInteractableException:
        print("Element not interactable.")


# mitmproxy가 실행되는 호스트와 포트
proxy = "localhost:18080"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server={proxy}")

# SNS 로그인 정보
EMAIL = "gate_flowers@naver.com"
PASSWORD = "arch0115"

capabilities = webdriver.DesiredCapabilities.CHROME.copy()
capabilities["acceptInsecureCerts"] = True

#chrome_options.set_capability("unhandledPromptBehavior", "ignore")
#
service = Service(ChromeDriverManager().install())
chromedriver_version = "114.0.5735.16"
browser = webdriver.Chrome(service=service, options=chrome_options)

# WebDriver 설정
#browser = webdriver.Chrome(
#    ChromeDriverManager().install(),
#    options=chrome_options,
#    desired_capabilities=capabilities,
#)
browser.maximize_window()
browser.get("https://www.spotvnow.co.kr/")
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

time.sleep(2)
#close_all_popups(browser)
#time.sleep(2)

# 파일 삭제
path = "/Users/archmacmini/Project/jpotv/proxy/"
with open(f'{path}/output.txt', 'w') as file:
    pass

# TV 채널 클릭
#tv_channel = browser.find_element_by_css_selector("li.header-ch span")
#actions = ActionChains(browser)
#actions.move_to_element(tv_channel).perform()

# 대기 시간
#time.sleep(2)
# TV 채널 클릭
#tv_channel.click()

#try:
#    image_element = WebDriverWait(browser, 10).until(
#        EC.presence_of_element_located((By.CSS_SELECTOR, "div.Program-Channel.bg-214"))
#    )
#    # 요소 클릭
#    image_element.click()
#except TimeoutError:
#    print("해당 요소를 찾지 못했습니다.")

#time.sleep(5)
cookies = {}
for i in CHANNEL_LIST:
    browser.get(f"https://www.spotvnow.co.kr/player?type=channel&id={i}")    
    cookies = browser.get_cookies()
    for cookie in cookies:
        if cookie['name'] == 'CloudFront-Key-Pair-Id':
            key_pair = cookie['value']
        if cookie['name'] == 'CloudFront-Policy':
            policy = cookie['value']
        if cookie['name'] == 'CloudFront-Signature':
            sig = cookie['value']
    time.sleep(2)

new_string = f"chunklist_b1692000.m3u8?Policy={policy}&Signature={sig}&Key-Pair-Id={key_pair}"
filename = '/Users/archmacmini/Project/jpotv/proxy/output.txt'  # 원하는 파일 이름으로 변경해주세요.

# 파일에서 내용 읽기
with open(filename, 'r') as file:
    lines = file.readlines()

# 각 줄을 처리
modified_lines = []
for line in lines:
    parts = line.strip().split('/')
    if parts:
        parts.pop()
    parts.append(new_string)
    modified_line = '/'.join(parts)
    modified_lines.append(modified_line + '\n')

# 수정된 내용으로 파일에 다시 쓰기
with open(filename, 'w') as file:
    file.writelines(modified_lines)

browser.quit()
