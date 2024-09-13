import os
import stat
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

PATH = "/Users/archmacmini/Project/jpotv/result"

def set_chromedriver_permissions(path):
    # 사용자 권한을 읽기, 쓰기, 실행 가능하게 설정
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    # 그룹 및 다른 사용자도 실행 가능하게 설정
    os.chmod(path, stat.S_IRUSR | stat.S_IXUSR)

# 크롬 옵션 설정 (headless 모드)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")  # 전체 페이지 스크린샷을 위해 필요한 옵션

driver_path = ChromeDriverManager().install()

last_slash_index = driver_path.rfind("/")

# chromedirver issue
new_path = driver_path[:last_slash_index] + "/chromedriver"
set_chromedriver_permissions(new_path)

service = Service(new_path)
# chromedriver_version = "114.0.5735.16"
driver = webdriver.Chrome(service=service, options=chrome_options)

# 원하는 URL 접속
# sample url 
# https://ch07-elivecdn.spotvnow.co.kr/ch07/cbcs/medialist_9171188557012390620_hls.m3u8

image_folder = f"{PATH}/thumbnail"

if os.path.exists(image_folder):
    for file_name in os.listdir(image_folder):
        if file_name.endswith(".png"):
            file_path = os.path.join(image_folder, file_name)
            os.remove(file_path)
            print(f"{file_name} 삭제 완료")
else:
    # 폴더가 없는 경우 폴더 생성
    os.makedirs(image_folder)
    print(f"폴더 {image_folder} 생성 완료")

for i in range(1,21):
    ch_name = f"ch{i}"
    if i < 10:
        ch_name = f"ch0{i}"
    
    url = f"https://{ch_name}-elivecdn.spotvnow.co.kr/{ch_name}/cbcs/medialist_9171188557012390620_hls.m3u8"        
    driver.get(url)

    # 페이지 로딩 대기
    time.sleep(5)

    # 스크린샷 저장
    screenshot_path = f"{image_folder}/{ch_name}.png"
    driver.save_screenshot(screenshot_path)

# 브라우저 종료
driver.quit()


