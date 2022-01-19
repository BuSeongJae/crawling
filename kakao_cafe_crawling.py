import csv
import re

from selenium import webdriver as wd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# from Rest import Restinfo
# from DB_Helper import DBHelper




def run():
    driver = wd.Chrome(executable_path='./chromedriver.exe')


    main_url = 'https://map.kakao.com/?nil_profile=title&nil_src=local'

    keyword = '홍대술집'
    filename = 'hongdae'

    #크롤링 자료 저장 리스트
    Rest_list = []

    driver.get(main_url)

    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]') #검색창
    search_area.send_keys(keyword)
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER) #검색실행
    time.sleep(2)

    driver.find_element_by_xpath('//*[@id="info.main.options"]/li[2]/a').send_keys(Keys.ENTER) #장소클릭
    time.sleep(0.2)

    #store_info() start###################################################
    def store_info():
        time.sleep(0.2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        cafe_lists = soup.select('.placelist> .PlaceItem')

        count = 1
        for cafe in cafe_lists:

            temp = []
            cafe_name = cafe.select('.head_item > .tit_name> .link_name')[0].text
            food_score = cafe.select('.rating> .score > .num')[0].text
            review = cafe.select('.rating > .review')[0].text
            link = cafe.select('.contact > .moreview')[0]['href']
            addr = cafe.select('.addr')[0].text
            phone = cafe.select('.info_item > .clickArea > .phone')[0].text

            review = review[3: len(review)]

            review = int(re.sub(",","",review))

            print(cafe_name, food_score, review, link, addr, phone)

            temp.append(cafe_name)
            temp.append(food_score)
            temp.append(review)
            temp.append(link)
            temp.append(addr)
            temp.append(phone)

            Rest_list.append(temp)

        f = open(filename+'.csv', "w", encoding="utf-8-sig", newline="")
        writercsv = csv.writer(f)
        header = ['Name', 'Score', 'Review', 'Link', 'Addr']
        writercsv.writerow(header)

        for i in Rest_list:
            writercsv.writerow(i)
    #store_info() end###########################################

    page = 1 #실제페이지
    page2 = 0 # 5페이지 이후 다음을 누르면 0으로 초기화 되는 용도


    for i in range(0, 34): #34페이지까지 반복 크롤링

        try:

            page2 += 1

            print(page, "page 이동")

            driver.find_element_by_xpath(f'//*[@id="info.search.page.no{page2}"]').send_keys(Keys.ENTER) # 페이지 클릭 page2가 바뀌면서(.format과 같은기능) 실행됨

            store_info() # store_info()함수 실행시켜서 크롤링

            if (page2)%5 ==0: # 5페이지 크롤링 된 후 page2를 0으로 초기화해서 다음 섹션의 0~5 선택 반복
                driver.find_element_by_xpath('//*[@id="info.search.page.next"]').send_keys(Keys.ENTER) # 페이지 다음으로 넘기기 버튼 클릭

                page2 = 0


            page += 1

        except Exception as e:
            print(e)
            break














run()
