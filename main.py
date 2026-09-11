
```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write(
    "1년치 일별 박스오피스 데이터를 이용해 "
    "영화 데이터의 시간에 따른 변화를 살펴봅니다."
)


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
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
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # 날짜순으로 정렬
    df = df.sort_values(
        ["날짜", "순위"]
    ).reset_index(drop=True)

    return df


df = load_data()


# ============================================================
# 데이터 정보
# ============================================================

st.divider()
st.header("📊 데이터 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "전체 데이터 수",
        f"{len(df):,}개"
    )

with col2:
    st.metric(
        "기록 날짜 수",
        f"{df['날짜'].nunique():,}일"
    )

with col3:
    st.metric(
        "영화 종류",
        f"{df['영화명'].nunique():,}편"
    )


# ============================================================
# 그래프 1
# 영화별 일관객 변화
# ============================================================

st.divider()
st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 하나 선택하면 그 영화의 날짜별 일관객 변화를 "
    "확인할 수 있습니다."
)


movie_list = sorted(
    df["영화명"].dropna().unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list
)


movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig1.update_traces(
    hovertemplate=
    "날짜: %{x|%Y년 %m월 %d일}"
    "<br>관객수: %{y:,}명"
    "<extra></extra>"
)

fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    hovermode="x unified"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# ============================================================
# 그래프 1 해석 직접 입력
# ============================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 내용을 직접 입력하세요.",
    placeholder="여기에 직접 입력하세요.",
    height=100,
    key="graph1_explanation"
)


# ============================================================
# 그래프 2
# 일관객 합계가 가장 큰 영화 5편
# ============================================================

st.divider()
st.header("📈 그래프 2. 일관객 합계가 가장 큰 영화 5편")

st.write(
    "전체 기간 동안 일관객을 모두 합산하여 "
    "합계가 가장 큰 5편의 날짜별 일관객 변화를 비교합니다."
)


# 영화별 전체 기간 일관객 합계
movie_total = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values(
        "일관객",
        ascending=False
    )
)

top5_movies = movie_total.head(5)["영화명"].tolist()


# TOP 5 영화의 날짜별 데이터
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)


fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="기간 내 일관객 합계 TOP 5 영화의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=
    "영화: %{fullData.name}"
    "<br>날짜: %{x|%Y년 %m월 %d일}"
    "<br>관객수: %{y:,}명"
    "<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    hovermode="x unified",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# TOP 5 목록
st.subheader("🏆 일관객 합계 TOP 5")

for i, movie in enumerate(top5_movies, start=1):
    total = movie_total.loc[
        movie_total["영화명"] == movie,
        "일관객"
    ].iloc[0]

    st.write(
        f"**{i}위. {movie}** — "
        f"기간 일관객 합계: {total:,.0f}명"
    )


# 그래프 2 해석
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 내용을 직접 입력하세요.",
    placeholder="여기에 직접 입력하세요.",
    height=100,
    key="graph2_explanation"
)


# ============================================================
# 그래프 3
# 날짜별 10위권 일관객 합계
# ============================================================

st.divider()
st.header("📊 그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "각 날짜의 박스오피스 10위권 영화들의 일관객을 모두 합산하여 "
    "날짜별 전체 관객 규모의 변화를 보여줍니다."
)


# ------------------------------------------------------------
# 날짜별 10위권 일관객 합계 계산
# ------------------------------------------------------------

daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)


# ------------------------------------------------------------
# 일관객 합계가 가장 큰 날 TOP 3
# ------------------------------------------------------------

top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("날짜")
)


# ------------------------------------------------------------
# 영역 그래프
# ------------------------------------------------------------

fig3 = go.Figure()


fig3.add_trace(
    go.Scatter(
        x=daily_total["날짜"],
        y=daily_total["일관객"],
        mode="lines",
        name="10위권 일관객 합계",
        fill="tozeroy",
        hovertemplate=
        "날짜: %{x|%Y년 %m월 %d일}"
        "<br>10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)


# ------------------------------------------------------------
# TOP 3 날짜 표시
# ------------------------------------------------------------

fig3.add_trace(
    go.Scatter(
        x=top3_days["날짜"],
        y=top3_days["일관객"],
        mode="markers+text",
        name="합계 TOP 3",
        text=[
            f"{date.strftime('%Y년 %m월 %d일')}"
            for date in top3_days["날짜"]
        ],
        textposition="top center",
        marker=dict(
            size=10
        ),
        hovertemplate=
        "날짜: %{x|%Y년 %m월 %d일}"
        "<br>10위권 일관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)


fig3.update_layout(
    title="날짜별 10위권 일관객 합계",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계",
    hovermode="x unified"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)


# ------------------------------------------------------------
# TOP 3 날짜 목록
# ------------------------------------------------------------

st.subheader("🏆 10위권 일관객 합계가 가장 컸던 날")

top3_display = top3_days.sort_values(
    "일관객",
    ascending=False
).reset_index(drop=True)

for i, row in top3_display.iterrows():
    date_text = row["날짜"].strftime("%Y년 %m월 %d일")

    st.write(
        f"**{i + 1}위. {date_text}** — "
        f"10위권 일관객 합계: {row['일관객']:,.0f}명"
    )


# ============================================================
# 그래프 3 해석 직접 입력
# ============================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 내용을 직접 입력하세요.",
    placeholder="여기에 직접 입력하세요.",
    height=100,
    key="graph3_explanation"
)


# ============================================================
# 그래프 4 영역
# ============================================================

st.divider()
st.header("📊 그래프 4")

st.write(
    "다음 그래프를 이곳에 추가할 수 있습니다."
)

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 4에서 알 수 있는 내용을 직접 입력하세요.",
    placeholder="여기에 직접 입력하세요.",
    height=100,
    key="graph4_explanation"
)
```
