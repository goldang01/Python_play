from urllib.request import urlopen
from bs4 import BeautifulSoup

import re
import pandas as pd
from datetime import datetime, timedelta

# https://search.shopping.naver.com/best100v2/detail.nhn?catId=50000190

category_df = pd.DataFrame({
    'category' : ['스킨케어', '베이스메이크업', '색조메이크업', '클렌징', 
                  '마스크/팩', '선케어', '남성화장품', '향수', 
                  '바디케어', '헤어케어', '헤어스타일링', '네일케어',
                 '뷰티소품'],
    'category_code' : ['50000190', '50000194', '50000195', '50000192', 
                       '50000193','50000191', '50000202', '50000200',
                      '50000197', '50000198', '50000199', '50000196',
                      '50000201']
})

total = pd.DataFrame()

today_dt = datetime.today()

for catid in range(len(category_df)):
    category_nm = category_df['category'][catid]
    category_code = category_df['category_code'][catid]

    url = 'https://search.shopping.naver.com/best100v2/detail.nhn?catId=' + category_code
    
    
    html = urlopen(url)
    bsObject = BeautifulSoup(html, "html.parser")

    tag = 'li'
    className = '_itemSection'
    content = bsObject.body.find_all(tag,{"class", className})


    # for i in range(3):
    for i in range(len(content)):
        tag = "p"
        className = "cont"
        title = content[i].find(tag,{"class", className})
        title_name = title.text.replace('\n',"")

        tag = "div"
        className = "price"
        price = content[i].find(tag,{"class", className})
        price_name = price.text.replace('\n','')
        
        price_num = numbers = re.sub(r'[^0-9]', '', price_name)
        
        df = pd.DataFrame({
            'date' : [today_dt],
            'category' : [category_nm],
            'title' : [title_name],
            'price' : [price_num],
        })
        total = pd.concat([total, df])

# 저장
total.to_csv("top_100.csv", index = False)

# # .to_csv 
# # 최초 생성 이후 mode는 append
# if not os.path.exists('top_100.csv'):
#     df.to_csv('top_100.csv', index=False, mode='w')
# else:
#     df.to_csv('top_100.csv', index=False, mode='a', header=False)
