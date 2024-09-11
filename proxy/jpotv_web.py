import cv2
import time
import json
import requests
import stat
import os

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
PATH = "/Users/archmacmini/Project/jpotv/result"
DEFAULT_SIZE = 118767161

def set_chromedriver_permissions(path):
    # 사용자 권한을 읽기, 쓰기, 실행 가능하게 설정
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    # 그룹 및 다른 사용자도 실행 가능하게 설정
    os.chmod(path, stat.S_IRUSR | stat.S_IXUSR)

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

def check_onair(browser, channel):
    img_path=f"{PATH}/{channel}.png"
    browser.get_screenshot_as_file(img_path)
    
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    image_size = 0
    standart_size = 1

    for line in image:
        for cell in line:
            image_size += line[cell]
    
    if abs(image_size / DEFAULT_SIZE) > 1.05 or abs(image_size / DEFAULT_SIZE) < 0.95:
        return channel
    return None

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

driver_path = ChromeDriverManager().install()

# chromedirver issue
new_path = driver_path[:last_slash_index] + "/chromedriver"
set_chromedriver_permissions(new_path)

service = Service(new_path)

#service = Service(ChromeDriverManager().install())
#chromedriver_version = "114.0.5735.16"
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
    tmp_elements= browser.find_elements(By.XPATH, "//p[contains(text(), '하이라이트')]")
    if tmp_elements[i].text.startswith("하이라이트"):
        continue
    highlight_names.append(tmp_elements[i].text)
    tmp_elements[i].click()
    time.sleep(3)
    browser.get(home_url)
    time.sleep(3)
    #elements= browser.find_elements(By.XPATH, "//p[contains(text(), '하이라이트')]")
    time.sleep(3)

filename = '/Users/archmacmini/Project/jpotv/result/output.txt' # path 수정 필요
with open(filename, 'r') as file:
    lines = file.readlines()
cred_line = lines[0].split("?")[1]


#for main scene
browser.get(home_url)
time.sleep(3)

elements= browser.find_elements(By.XPATH, "//p[contains(text(), '주요장면')]")

for element in elements:
    print(element.text)

for i in range(0, len(elements)):
    tmp_elements= browser.find_elements(By.XPATH, "//p[contains(text(), '주요장면')]")
    if tmp_elements[i].text.startswith("주요장면"):
        continue
    highlight_names.append(tmp_elements[i].text)
    tmp_elements[i].click()
    time.sleep(3)
    browser.get(home_url)
    time.sleep(3)
    #elements= browser.find_elements(By.XPATH, "//p[contains(text(), '주요장면')]")
    time.sleep(3)
# end main scene


onair_channel = []
#extra channel
for i in range(1, 10):
    str_channel = f"0{i}"
    url=f"https://ch0{i}-livecdn.spotvnow.co.kr/ch0{i}/spt0{i}_pc.smil/playlist.m3u8?{cred_line}"
    res = requests.get(url)
    if res.status_code == 200:
        print("channel searched")
        browser.get(url)
        time.sleep(3)
        if check_onair(browser,str_channel):
            onair_channel.append(str_channel)
        

#extra channel 2
for i in range(10,40):
    url=f"https://ch{i}-livecdn.spotvnow.co.kr/ch{i}/spt{i}_pc.smil/playlist.m3u8?{cred_line}"
    res = requests.get(url)
    if res.status_code == 200:
        print("channel searched")
        browser.get(url)
        time.sleep(3)
        if check_onair(browser,str(i)):
            onair_channel.append(str(i))


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
        if name in onair_channel:
            json_tmp = {
                "1080": line
            }



with open(f'{PATH}/output.json', 'w', encoding='utf-8') as file:
    json.dump(res_json, file, ensure_ascii=False, indent=4)    

browser.quit()

'''
https://ch32-livecdn.spotvnow.co.kr/ch32/spt32_pc.smil/chunklist_playlist.m3u8?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vc3BvdHYtbGl2ZWNkbi5zcG90dm5vdy5jby5rci9zcG90di9zcG90dl9wYy5zbWlsLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3MTE4ODQzMjB9fX1dfQ__&Signature=Uc9R7oz-EesDgS6Zfkauj6q5Y3t8DnsIoUKir5mM9QDCETejlJXbBFUCFUUEw1kjpUbhf3arYa4NSgbtUE~QxgS~ZEm~PZjoGknxJNl7~Mat3GmcaSZaawp4eZMG5sLvnr0WD58yWKi6h92hYZHbr7PHTeQJCySYaPLAlJf8zircz1haftP85Ua9dkG4fhPiG~pyYkAuYCohMclJenTu0whOQmY23DuhuJS3MM2faMbuVfdE~q-zuR2CXwd90iEgbeyUDfNicVuW71yCz4lDUtuClNdAXDPDl7Ud-JLQcJCyjEPTsSnIBcFHpz-EumrmmroTyDu4KaktxsLk83gMrQ__&Key-Pair-Id=APKAI2M6I5EDDXED7H5Q


https://ch28-livecdn.spotvnow.co.kr/ch28/spt28_pc.smil/playlist.m3u8?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vY2gyOC1saXZlY2RuLnNwb3R2bm93LmNvLmtyL2NoMjgvc3B0MjhfcGMuc21pbC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzExOTMzODAwfX19XX0_&Signature=Any10rKz28oV5QA6A64VrZLgdAXR0qKIFBfRPidGEdZIr63ePooGCaNW~9h2GrvK1C3oq6byc61EHXnsihS9C9ve-HvGf-Axb0jgdYk-3iawovGb0Q3QEMufS3BkYSl008ah6iOQYsgAJbpjNxGzuBhk04G3Bt4b0QQtWfEFYd54QZILuuqvsTU0l4JNyqi-sSlyRXsjfroFlNViODPXRCA7b2nwSFkKzdkHumukbTgryRYpGyOEansIHs03C9lifvPY9e0K9-dgfRc3QST3-~3P9iPZeRa5RMONM4B6OxxfgtjREL0giLAK10AlP38tstZtHqZbuXamrg-ei-8MGA__&Key-Pair-Id=APKAI2M6I5EDDXED7H5Q
https://spotv-livecdn.spotvnow.co.kr/spotv/spotv_pc.smil/chunklist_b9192000.m3u8?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vc3BvdHYtbGl2ZWNkbi5zcG90dm5vdy5jby5rci9zcG90di9zcG90dl9wYy5zbWlsLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3MTE5MzExMjB9fX1dfQ__&Signature=CmBV-rxI1LWllhsqQU73OJmCpx8YbPNRuGYtPDqnfTtgPcvjN7fUUFzZumsKNEk2TM6ETr7tWeU9%7EHCvcl-5ODKA2rWil1VuHsE2r4JFHhFa1XbGR3O-Qx0lgQIOA2M6mgNoO41Q3RBrkcEOWI8vPEIyX9vYgnfRPor9AQp5oL4HHAXPh7Ti2BQ5u4Atmlhd-3AFM0%7E-E9QCz-Sgjt5IZfOrc5qZFYPgoSSxDG57FU2k2RP56BPE-Ux%7E4vbHvopWRYSJ6XmQ7WE%7EamsfU56PBfOe4tp%7EwyRXRgPUB%7EzHOkP1pdX8-Sm1BcXxALxu0D2g7uqb73TCp2NMHKJXaizPoQ__&Key-Pair-Id=APKAI2M6I5EDDXED7H5Q

https://ch03-livecdn.spotvnow.co.kr/ch03/spt03_pc.smil/playlist.m3u8?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vc3BvdHYtbGl2ZWNkbi5zcG90dm5vdy5jby5rci9zcG90di9zcG90dl9wYy5zbWlsLyoiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3MTE5MzExMjB9fX1dfQ__&Signature=CmBV-rxI1LWllhsqQU73OJmCpx8YbPNRuGYtPDqnfTtgPcvjN7fUUFzZumsKNEk2TM6ETr7tWeU9%7EHCvcl-5ODKA2rWil1VuHsE2r4JFHhFa1XbGR3O-Qx0lgQIOA2M6mgNoO41Q3RBrkcEOWI8vPEIyX9vYgnfRPor9AQp5oL4HHAXPh7Ti2BQ5u4Atmlhd-3AFM0%7E-E9QCz-Sgjt5IZfOrc5qZFYPgoSSxDG57FU2k2RP56BPE-Ux%7E4vbHvopWRYSJ6XmQ7WE%7EamsfU56PBfOe4tp%7EwyRXRgPUB%7EzHOkP1pdX8-Sm1BcXxALxu0D2g7uqb73TCp2NMHKJXaizPoQ__&Key-Pair-Id=APKAI2M6I5EDDXED7H5Q


https://ch03-livecdn.spotvnow.co.kr/ch03/spt03_pc.smil/playlist.m3u8?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vY2gwMy1saXZlY2RuLnNwb3R2bm93LmNvLmtyL2NoMDMvc3B0MDNfcGMuc21pbC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzExOTI2OTAwfX19XX0_&Signature=tX1zTK7~R909BUJkQW0VKwJFKZi10057d0uzLgDn~0KdEWtchOcAGU~DVP~Qc1cU9x63t4ckyI2scuQg2vRM6AZCMyA9AO28MiEYWUXSZse3l2aeHpOrF7GN0vLSbz6MGnW84~4Qt7slF7MEjf3dzLvSpgKvdu~nRBEepTOzrZqTYLIIpnxz8YCbdpbI3YqbRuCZbLNEbkXKEMF7zdrk5A-hYewoihPSt2Fkf6Q0C59sJ45pnIvuxntSLEN8~MhpqDHbre7WkJEoX-yfK~qH5dEuZjMb3fUjytzNnp-vrTfdoOXwe62rGDHBXjn-YZ-Ffnd2bumENOFmGMx8MT~Q9Q__&Key-Pair-Id=APKAI2M6I5EDDXED7H5Q
'''