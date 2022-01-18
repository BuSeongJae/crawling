from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys

def traffic_run():

    driver = wd.Chrome(executable_path='./chromedriver.exe')
    main_url = 'https://map.naver.com/v5/directions/-/-/-/transit?c=14131707.3018997,4519071.1649168,12,0,0,0,dhb'
    # 검색 결과 담을 리스트
    traffic_list=[]
    #사이트 접속
    driver.get(main_url)
    starting_point = '홍대입구'
    arrival_point = '신도림역'
    try:
        driver.find_element(By.XPATH, '//*[@id="container"]/shrinkable-layout/div/directions-layout/directions-result/div[1]/div/ul/li[2]/a').click()
        time.sleep(1)

        element = driver.find_element(By.ID, 'directionStart0')
        time.sleep(0.02)
        element.send_keys(starting_point)
        time.sleep(0.02)
        element.send_keys(Keys.RETURN)
        time.sleep(0.5)
        element.send_keys(Keys.RETURN)

        element = driver.find_element(By.ID, 'directionGoal1')
        time.sleep(0.02)
        element.send_keys(arrival_point)
        time.sleep(0.02)
        element.send_keys(Keys.RETURN)
        time.sleep(0.5)
        element.send_keys(Keys.RETURN)
        time.sleep(0.5)


        driver.find_element(By.XPATH, '//*[@id="directionStart0"]').click()
        time.sleep(1)

    except Exception as e:
        print('경로찾기 오류', e)
    ### 경로찾기 끝 ###

    ### 찾은경로에서 세부사항 크롤링###

    soup = bs(driver.page_source, 'html.parser')
    # 자동차 소요시간
    print(soup.select('.scroll_inner > .list_summary > .ng-star-inserted> .summary_box> .summary_title')[0].text)

    # 도로상황, 경로, 거리
    print(soup.select('.scroll_inner > .list_summary > .ng-star-inserted> div.route_box')[0].text)

    ### 세부사항 크롤링 끝###

    time.sleep(10)

    driver.close()  # 크롬 브라우저 닫기
    driver.quit()  # 드라이버 종료
    import sys

    sys.exit()

traffic_run()
