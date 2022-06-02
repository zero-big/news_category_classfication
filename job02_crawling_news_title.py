from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
#제로 값이나 여러 에러 들을 무시 할 때 사용
import pandas as pd
import re
import time

#selenium은 브라우저를 사용하여 크롤링할때 필수로 사용함.

pages =[110, 110, 110, 78, 110, 66]
category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101#&date=%2000:00:00&page=1'

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')


# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('disable-gpu')   #3가지는 리눅스 운영체제일땐 사용해야함

driver = webdriver.Chrome('./chromedriver', options=options)
df_titles = pd.DataFrame()

for i in range(0, 6):  #뉴스 섹선(정치,사회...)
    titles = []
    for j in range(1, pages[i]+1): #J = 페이지
        url ='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
        driver.get(url)
        time.sleep(0.2) #0.2초간 잠을 재움(동작을 0.2초 지연시킴)
        # (//*[@id="section_body"]/ul[1]/li[5]/dl/dt[2]/a / a   #페이지 코드표 copy 항목에서 xpath를 가져오면 됨

        for k in range(1, 5):
            for l in range(1, 6):
                x_path =' //*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l) #x_path 섹션을 찾을때 사용
                try:
                    title = driver.find_element_by_xpath(x_path).text
                    title = re.compile('[^가-힣 ]').sub('', title)
                    titles.append(title)

                except NoSuchElementException as e: #Xpath가 없어서 못받는 에러 메시지(로딩이 늦어서 xpath를 잘 못받을떄도 나옴)
                    time.sleep(0.5)
                    try:
                        title = driver.find_element_by_xpath(x_path).text
                        #시간이 없어서 xpath를 못받아 올때 시간을 더 주고 위의 명령을 재수행함.
                        title = re.compile('[^가-힣 ]').sub('', title)
                        titles.append(title)
                    except:
                        try:
                            x_path = ' //*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)
                            title = driver.find_element_by_xpath(x_path).text
                            title = re.compile('[^가-힣 ]').sub('', title)
                        except:
                            print('no such element')

                except StaleElementReferenceException as e: # 페이지를 못찾아서 나오는 에러메시지
                    print(e)
                    print(category[i], 'page', j, k*l)  #j섹션의 K의 ㅣ번째 기사를 나타냄
                except:
                    print('error')
        if j % 30 == 0:
            print('save', len(titles))
            df_section_titles = pd.DataFrame(titles, columns=['titles'])
            df_section_titles['category'] = category[i] #위 카테고리 리스트를 인덱싱해서 카테고리별 명으로 분류를함.
            df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)  #concat : 판다스에서 합치는 함수
            df_section_titles.to_csv('./crawling_data/crawling_data_{}_{}_{}.csv'.format(category[i], j-29, j), index=False, encoding='utf-8-sig')
                                                    #j가 페이지- 30쪽마다 저장함이므로 -29하면 1쪽부터 30까지
            titles =[]

    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]  # 위 카테고리 리스트를 인덱싱해서 카테고리별 명으로 분류를함.
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)  # concat : 판다스에서 합치는 함수
    df_section_titles.to_csv('./crawling_data/crawling_data_{}_last.csv'.format(category[i]), index=False, encoding='utf-8-sig')
    # j가 페이지- 30쪽마다 저장함이므로 -29하면 1쪽부터 30까지
df_section_titles = pd.DataFrame(titles, columns=['titles'])
df_section_titles['category'] = category[i]  # 위 카테고리 리스트를 인덱싱해서 카테고리별 명으로 분류를함.
df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)  # concat : 판다스에서 합치는 함수 크롤링 데이터가 누적이됨
df_titles.to_csv('./crawling_data/naver_news_titles_test{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False, encoding='utf-8-sig') #엑셀의 인덱스는 없이 utf-8로 함.
# j페이지에서 30쪽이 넘어 남는 쪽수에 대한 묶음


driver.close()  # 크롤링 끝난 후 필수로 닫아야함.
# //*[@id="section_body"]/ul[2]/li[5]/dl/dt[2]/a
# //*[@id="section_body"]/ul[3]/li[1]/dl/dt[2]/a
# //*[@id="section_body"]/ul[3]/li[1]/dl/dt/a  #사진이 없는 경우 인덱싱을 하지 않아서 [2]가 없음
# df_titles.to_csv('.crawling_data.csv', index=False)

# //*[@id="section_body"]/ul[3]/li[5]/dl/dt[2]/a
# //*[@id="section_body"]/ul[4]/li[1]/dl/dt[2]/a







