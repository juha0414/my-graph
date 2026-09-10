import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("1년치 일별 박스오피스 데이터를 이용해 영화 관객수의 시간에 따른 변화를 살펴봅니다.")


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 데이터 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # 날짜순으로 정렬
    df = df.sort_values(["날짜", "순위"]).reset_index(drop=True)

    return df


df = load_data()


# ============================================================
# 데이터 안내
# ============================================================

st.subheader("📊 데이터 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("전체 데이터 수", f"{len(df):,}개")

with col2:
    st.metric("기록 날짜 수", f"{df['날짜'].nunique():,}일")

with col3:
    st.metric("영화 종류", f"{df['영화명'].nunique():,}편")


# ============================================================
# 그래프 1
# 영화별 날짜에 따른 일관객 변화
# ============================================================

st.divider()
st.header("1. 영화별 일관객 변화")
st.write("영화를 하나 선택하면 날짜에 따른 하루 관객수의 변화를 확인할 수 있습니다.")


# 영화 목록
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list
)


# 선택한 영화 데이터
movie_df = df[df["영화명"] == selected_movie].copy()

movie_df = movie_df.sort_values("날짜")


# 선 그래프
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y년 %m월 %d일",
        "일관객": ":,"
    }
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y년 %m월 %d일}<br>관객수: %{y:,}명<extra></extra>"
)

fig.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 그래프 해석 문구
# ============================================================

st.markdown("### 💡 이 그래프로 알 수 있는 것")

st.info(
    f"「{selected_movie}」의 하루 관객수가 날짜에 따라 어떻게 증가하거나 감소했는지 "
    "확인할 수 있습니다."
)


# ============================================================
# 다음 그래프를 추가할 공간
# ============================================================

st.divider()
st.header("2. 다음 그래프")
st.caption("앞으로 새로운 그래프를 추가할 예정입니다.")


# 여기에 두 번째 그래프를 추가하면 됩니다.


st.divider()
st.header("3. 다음 그래프")
st.caption("앞으로 새로운 그래프를 추가할 예정입니다.")


# 여기에 세 번째 그래프를 추가하면 됩니다.
