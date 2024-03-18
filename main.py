import requests
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime   # 날짜
from streamlit_option_menu import option_menu
import os

st.set_option('deprecation.showPyplotGlobalUse', False)

# 사이드바에 위젯 추가
with st.sidebar:
  selected = option_menu(
    menu_title = "Menu",
    options = ["Project"],
    icons = ["book"],
    menu_icon = "app-indicator",
    default_index = 0,
  )


def ObtainingData(decoded_data: str) -> None:
    data_dict = json.loads(decoded_data)

    
    # 필요한 데이터를 추출하여 DataFrame으로 변환
    items = data_dict['response']['body']['items']['item']
    st.write('구조 유기견 : ', len(items),"마리")
    staryDogInf = []

    # 데이터 전처리
    for item in items:
        # 성별
        if 'M' in item['sexCd']:
            item['sexCd'] = '남'
        elif 'F' in item['sexCd']:
            item['sexCd'] = '여'
        # 지역
        if '서울' in item['orgNm']:
            item['orgNm'] = '서울'
        elif '경기' in item['orgNm']:
            item['orgNm'] = '경기'
        elif '인천' in item['orgNm']:
            item['orgNm'] = '인천'
        elif '세종' in item['orgNm']:
            item['orgNm'] = '세종'
        elif '충청' in item['orgNm']:
            item['orgNm'] = '충청'
        elif '강원' in item['orgNm']:
            item['orgNm'] = '강원'
        elif '전라' in item['orgNm']:
            item['orgNm'] = '전라'
        elif '경상' in item['orgNm']:
            item['orgNm'] = '경상'
        elif '제주' in item['orgNm']:
            item['orgNm'] = '제주'
        elif '부산' in item['orgNm']:
            item['orgNm'] = '부산'
        elif '대구' in item['orgNm']:
            item['orgNm'] = '대구'
        elif '광주' in item['orgNm']:
            item['orgNm'] = '광주'
        elif '울산' in item['orgNm']:
            item['orgNm'] = '울산'
        elif '대전' in item['orgNm']:
            item['orgNm'] = '대전'
        elif '전북' in item['orgNm']:
            item['orgNm'] = '전북'
        if '(년생)' in item['age']:
            item['age'] = int(item['age'].replace('(년생)', '').replace('(60일미만)', ''))
            item['age'] = str(2025 - item['age']) + '살'
        staryDogInf.append(item)

    df = pd.DataFrame(staryDogInf)
    # 'orgNm' 값의 빈도수 계산
    gender_count = df['sexCd'].value_counts()
    org_count = df['orgNm'].value_counts()
    age_count = df['age'].value_counts()

    # 그래프 그리기
    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False

    # 지역
    plt.figure(figsize=(10, 6))
    org_count.plot(kind='bar', color='skyblue')
    plt.title('구조 지역')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot()
    # 성별
    plt.figure(figsize=(10, 6))
    gender_count.plot(kind='bar', color='skyblue')
    plt.title('성별')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot()
    # 나이
    plt.figure(figsize=(10, 6))
    age_count.plot(kind='bar', color='skyblue')
    plt.title('나이')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot()
    # 몸무게
    plt.figure(figsize=(10, 6))
    df['weight'] = df['weight'].str.extract('(\d+)').astype(float)
    df['weight'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black')
    plt.title('몸무게')
    plt.ylabel('Count')
    plt.grid(True)
    st.pyplot()

if __name__ == "__main__":
    # 세팅
    now = datetime.now()
    formattedDate = now.strftime('%Y%m%d')
    yesterDay = str(int(formattedDate) - 1)
    st.title("일별 유기견 정보")
    selectedDate = st.date_input("날짜 선택")
    selectedDate = int(selectedDate.strftime('%Y%m%d')) - 1
    
    # API 요청
    API_KEY = os.environ["strayDog_APIKEY"]
    url = f'http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic?bgnde={selectedDate}&endde={selectedDate}&pageNo=1&upkind=417000&numOfRows=200&_type=json&serviceKey={API_KEY}'
    result = requests.get(url)
    decoded_data = result._content.decode('utf-8')
    ObtainingData(decoded_data)