from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'   #정치
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101' 경제
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102'  사회
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103'  문화
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104'  국제
# url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105'  IT
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.151 Whale/3.14.134.62 Safari/537.36'}
df_titles = pd.DataFrame()
# resp = requests.get(url, headers=headers)
# # print(resp)
# # print(list(resp))
# # print(type(resp))
#
# soup = BeautifulSoup(resp.text, 'html.parser')
# # print(soup)


#웹페이지 숫자에 따라서 for문으로 반복적으로 따옴.
for i in range(6):
    url='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url, headers=headers)
    # print(resp)
    # print(list(resp))
    # print(type(resp))
    soup = BeautifulSoup(resp.text, 'html.parser')
    # print(soup)
    # print(title_tags[0].text)
    title_tags = soup.select('.cluster_text_headline')  #위 문자열을 가진 것만 선택을 함
    titles=[]
    for title_tag in title_tags:
        # 숫자,영어,문장부호를 제외하고 한글만 남기기
        title = re.compile('[^가-힣 ]').sub('', title_tag.text)
        # title_tag에서 한글(가부터 힣를 (^표시는 제외라는 뜻)과 반대의 모든 것을 sub(제외하고) ('')로 바꾸려고 함. *''안에 다른 기호를 넣으면 그 기호로 바뀜
        # ^표시는 정규표현식 임. $,%등 다양함.
        titles.append(title)
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows'
                          , ignore_index=True)
print(df_titles.head())
df_titles.info()
print((df_titles['category']).value_counts())

df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
#{}안에 현재 시간을 넣을때 format(datetime 함수를 import 하여서 입력할 수 있음.)

