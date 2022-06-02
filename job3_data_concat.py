import pandas as pd
import glob
import datetime

data_path = glob.glob('./crawling_data/crawling*')
print(data_path)

df = pd.DataFrame()
for path in data_path[1:]:
    df_temp = pd.read_csv(path)
    df = pd.concat([df, df_temp])
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True)
print(df.head())
print(df.tail())
print(df['category'].value_counts())
df.info()
df.to_csv('./crawling_data/naver_news_titles_test{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False, encoding='utf-8-sig')
#
# data_path = glob.glob('./crawling_data/*')
# df = pd.DataFrame()
# for path in data_path[1:]:
#     df_temp = pd.read_csv(path)
#     df = pd.concat([df, df_temp])
# df.dropna(inplace=True)
# df.reset_index(inplace=True, drop=True)  #인덱스 있는 자료들을 합칠때는 인덱스를 버려야함으로 drop=True로 주어야 함.
# print(df.head())
# print(df.tail())
# print(df['category'].value_counts())
# df.info()
# df.to_csv('./crawling_data/naver_news_titles_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d')), index=False)
