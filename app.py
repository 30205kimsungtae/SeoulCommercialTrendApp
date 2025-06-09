import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("data/seoul_data.csv", encoding="cp949")
    return df

df = load_data()

st.title("서울시 상권 변화 지표 분석")
st.write("서울시에서 제공한 상권 변화 데이터를 기반으로 한 웹 앱입니다.")

# 지역 선택
area = st.selectbox("상권명 선택", df['상권_코드_명'].unique())

# 선택한 상권 데이터 필터링
filtered_df = df[df['상권_코드_명'] == area]

st.write(f"### 선택한 상권: {area}")
st.dataframe(filtered_df)

# 시각화: 분기별 평균 운영 영업 개월
if '기준_년분기_코드' in filtered_df.columns:
    trend = filtered_df[['기준_년분기_코드', '운영_영업_개월_평균']].sort_values('기준_년분기_코드')
    fig, ax = plt.subplots()
    ax.plot(trend['기준_년분기_코드'], trend['운영_영업_개월_평균'], marker='o')
    ax.set_title("분기별 평균 운영 영업 개월")
    ax.set_xlabel("기준 년분기")
    ax.set_ylabel("운영 영업 개월 평균")
    plt.xticks(rotation=45)
    st.pyplot(fig)
