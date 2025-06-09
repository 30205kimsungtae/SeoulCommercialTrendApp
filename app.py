import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 서울시 상권 변화 지표 분석")
st.write("서울시에서 제공한 상권 변화 데이터를 기반으로 한 시각화 웹 앱입니다.")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")  # 또는 utf-8-sig
        st.success("✅ CSV 로딩 성공!")

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

    except Exception as e:
        st.error(f"CSV 로딩 실패: {e}")
else:
    st.warning("📁 CSV 파일을 업로드해 주세요.")
