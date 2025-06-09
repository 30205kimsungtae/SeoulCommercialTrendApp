import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 로딩
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("/mnt/data/seoul_data.csv", encoding="cp949")  # ← 여기 경로 주의!
        return df
    except Exception as e:
        st.error(f"CSV 로딩 실패: {e}")
        return pd.DataFrame()

df = load_data()

st.title("📊 서울시 상권 변화 지표 분석")
st.write("서울시에서 제공한 상권 변화 데이터를 기반으로 한 시각화 웹 앱입니다.")

if df.empty:
    st.error("❌ 데이터가 비어 있습니다.")
else:
    # 상권명 선택
    area = st.selectbox("상권명 선택", df['상권_코드_명'].unique())
    filtered_df = df[df['상권_코드_명'] == area]

    st.write(f"### 선택한 상권: {area}")
    st.dataframe(filtered_df)

    # 시각화
    if '기준_년분기_코드' in filtered_df.columns and '운영_영업_개월_평균' in filtered_df.columns:
        trend = filtered_df[['기준_년분기_코드', '운영_영업_개월_평균']].sort_values('기준_년분기_코드')

        fig, ax = plt.subplots()
        ax.plot(trend['기준_년분기_코드'].astype(str), trend['운영_영업_개월_평균'], marker='o')
        ax.set_title("📈 분기별 평균 운영 영업 개월 수")
        ax.set_xlabel("기준 년분기")
        ax.set_ylabel("운영 개월 평균")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("📉 시각화에 필요한 컬럼이 없습니다.")

import os

file_path = "/mnt/data/seoul_data.csv"
print("파일 존재 여부:", os.path.exists(file_path))
