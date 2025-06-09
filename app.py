import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("data/서울시 상권분석서비스(상권변화지표-상권).csv", encoding="cp949")
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

# 시각화 (예: 분기별 점포 수 변화)
if '기준_년_코드' in df.columns and '분기_코드' in df.columns:
    trend = filtered_df.groupby(['기준_년_코드', '분기_코드'])['점포_수'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.plot(trend['기준_년_코드'].astype(str) + "-Q" + trend['분기_코드'].astype(str), trend['점포_수'], marker='o')
    ax.set_title("분기별 점포 수 변화")
    ax.set_xlabel("연도-분기")
    ax.set_ylabel("점포 수")
    st.pyplot(fig)
