import time
import json
import requests

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
        buttons = browser.find_elements(By.ID, "Close")
        # 'close'이라는 단어가 포함된 id를 가진 이미지 찾아 클릭
        for button in buttons:
            print("click button")
            button.click()
    except:
        print("There's no pop up")
    
    time.sleep(2)

# mitmproxy가 실행되는 호스트와 포트
proxy = "localhost:18080"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server={proxy}")
chrome_options.add_argument('--headless')
chrome_options.add_argument('window-size=1920x1080')

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

#파일 삭제
with open(f'/Users/archmacmini/Project/jpotv/result/output.txt', 'w') as file:
    pass

# go to tv channel
tv_channel_li = browser.find_element(By.CSS_SELECTOR, "li.header-ch")
tv_channel_li.click()
time.sleep(2)
div_element = browser.find_element(By.CSS_SELECTOR, "div.Program-Channel")
div_element.click()
time.sleep(5)

#search main channel
for i in CHANNEL_LIST:
    url = f"https://www.spotvnow.co.kr/player?type=channel&id={i}"
    browser.get(url)
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



#for highlights
browser.get(home_url)
time.sleep(3)

elements= browser.find_elements(By.XPATH, "//p[contains(text(), '하이라이트')]")

for element in elements:
    print(element.text)

highlight_names = []
for i in range(0, len(elements)):
    if elements[i].text.startswith("하이라이트"):
        continue
    highlight_names.append(elements[i].text)
    elements[i].click()
    time.sleep(3)
    browser.get(home_url)
    time.sleep(3)
    elements= browser.find_elements(By.XPATH, "//p[contains(text(), '하이라이트')]")
    time.sleep(3)

filename = '/Users/archmacmini/Project/jpotv/result/output.txt' # path 수정 필요
with open(filename, 'r') as file:
    lines = file.readlines()
cred_line = lines[0].split("?")[1]

#extra channel
for i in range(1, 10):
    
    url=f'https://ch0{i}-livescdn.spotvnow.co.kr/ch0{i}/spt0{i}_pc.smil/playlist.m3u8?{cred_line}'
    res = requests.get(url)
    if res.status_code == 200:
        browser.get(url)
        time.sleep(3)

#extra channel 2
for i in range(10,40):
    url=f'https://ch{i}-livescdn.spotvnow.co.kr/ch{i}/spt{i}_pc.smil/playlist.m3u8?{cred_line}'
    res = requests.get(url)
    if res.status_code == 200:
        browser.get(url)
        time.sleep(3)



# 파일에서 내용 읽기
with open(filename, 'r') as file:
    lines = file.readlines()

# 각 줄을 처리
modified_lines = []
for line in lines:
    if line.endswith("chunklist_b9192000.m3u8"):
        line=(line+cred_line)
    modified_lines.append(line)

# 수정된 내용으로 파일에 다시 쓰기
with open(filename, 'w') as file:
    file.writelines(modified_lines)

res_json= {}
#json parser
'''
1080: 9192000
720: 3692000
360: 1692000 
'''

count = 0
for line in modified_lines:
    if line.startswith("https://spotv"):
        prefix = line.split('-')[0]
        name = prefix.split('/')[-1]
        json_tmp = {
            "1080": line,
            "720": line.replace("9192000", "3692000"),
            "360": line.replace("9192000", "1692000")
        }
        res_json[name] = json_tmp
        
    if line.startswith("https://manifest"):
        json_tmp = {
            "1080": line
        }
        res_json[highlight_names[count]] = json_tmp
        count += 1
    
    if line.startswith("https://ch"):
        prefix = line.split('-')[0]
        name = prefix.split('/')[-1]
        json_tmp = {
            "1080": line
        }

path = "/Users/archmacmini/Project/jpotv/result"

with open(f'{path}/output.json', 'w', encoding='utf-8') as file:
    json.dump(res_json, file, ensure_ascii=False, indent=4)    

browser.quit()
