import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

PATH = "/Users/archmacmini/Project/jpotv/result"

# 크롬 옵션 설정 (headless 모드)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")  # 전체 페이지 스크린샷을 위해 필요한 옵션

# 크롬 드라이버 경로 지정
driver_path = '/path/to/chromedriver'
service = Service(driver_path)

# 브라우저 실행
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

