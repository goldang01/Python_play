import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.express as px

from PIL import Image

img = Image.open("JK_Co_aivelabs.png")
st.image(img, width=200, caption="")
	
st.title('네이버 화장품 Top 100 분석')

st.subheader('참고: [네이버 쇼핑 Beset 100](https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000190)')


st.sidebar.header('Menu')
name = st.sidebar.selectbox('Name', ['전체', '스킨케어', '베이스메이크업', '색조메이크업', '클렌징', 
                  '마스크/팩', '선케어', '남성화장품', '향수', 
                  '바디케어', '헤어케어', '헤어스타일링', '네일케어',
                 '뷰티소품'])
	
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
  'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
# DATA_URL = ('top_100.csv')  

total = pd.read_csv('top_100.csv')


# # https://coinmarketcap.com
# scraper = CmcScraper(name, start_date.strftime('%d-%m-%Y'), end_date.strftime('%d-%m-%Y'))
# 
# df = scraper.get_dataframe()


# Bar chart
@st.cache
def load_data(nrows):
  data = pd.read_csv(DATA_URL, nrows=nrows)
  lowercase = lambda x: str(x).lower()
  data.rename(lowercase, axis='columns', inplace=True)
  data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
  return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text(" ")

if st.checkbox('Show raw data'):
  st.subheader('Raw data')
  st.write(total)

# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)
	
# 카테고리별 평균
st.subheader("카테고리별 평균")
cate_mean = total.groupby('category').mean().sort_values(by="price", ascending=False)
cate_mean = cate_mean.reset_index()
fig_mean = px.bar(cate_mean, x='category', y='price')
st.plotly_chart(fig_mean)

# 카테고리별 최대값
st.subheader("카테고리별 최대값")
cate_max = total.groupby('category').max().sort_values(by="price", ascending=False)
cate_max = cate_max.reset_index()
fig_max = px.bar(cate_max, x='category', y='price')
st.plotly_chart(fig_max)

# 카테고리별 최소값
st.subheader("카테고리별 최소값")
cate_min = total.groupby('category').min().sort_values(by="price", ascending=False)
cate_min = cate_min.reset_index()
fig_min = px.bar(cate_min, x='category', y='price')
st.plotly_chart(fig_min)
