
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# --------------------------------------------------
# 1. 기본 설정
# --------------------------------------------------

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


# --------------------------------------------------
# 2. 데이터 불러오기
# --------------------------------------------------

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜형으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형으로 변환
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

    # 날짜와 순위 순으로 정렬
    df = df.sort_values(
        ["날짜", "순위"]
    ).reset_index(drop=True)

    return df


df = load_data()


# --------------------------------------------------
# 3. 데이터 정보
# --------------------------------------------------

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


# ==================================================
# 그래프 1
# ==================================================

st.divider()
st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 하나 선택하면 그 영화의 날짜별 "
    "일관객 변화를 확인할 수 있습니다."
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


st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 내용을 직접 입력하세요.",
    placeholder="여기에 직접 입력하세요.",
    height=100,
    key="graph1_explanation"
)


# ==================================================
# 그래프 2
# ==================================================

st.divider()
st.header("📈 그래프 2. 일관객 합계가 가장 큰 영화 5편")

st.write(
    "이 기간 동안 일관객을 모두 더해 "
    "합계가 가장 큰 5편의 날짜별 일관객을 비교합니다."
)


movie_total = (
    df.groupby(
        "영화명",
        as_index=False
    )["일관객"]
    .sum()
    .sort_values(
        "일관객",
        ascending=False
    )
)

top5_movies = movie_total.head(5)["영화명"].tolist()

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
    title="기간 일관객 합계 TOP 5 영화의 날짜별 일관객",
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


st.subheader("🏆 일관객 합계 TOP 5")

for i, movie in enumerate(
    top5_movies,
    start=1
):
    total = movie_total.loc[
        movie_total["영화명"] == movie,
        "일관객"
    ].iloc[0]

    st.write(
        f"**{i}위. {movie}** — "
        f"기간 일관객 합계: {total:,.0f}명"
    )


st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 내용을 직접 입력하세요.",
    placeholder="여기에 직접 입력하세요.",
    height=100,
    key="graph2_explanation"
)


# ==================================================
# 그래프 3
# ==================================================

st.divider()
st.header("📊 그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "각 날짜의 10위권 영화들의 일관객을 모두 더해 "
    "날짜별 관객 규모의 변화를 보여줍니다."
)


daily_total = (
    df.groupby(
        "날짜",
        as_index=False
    )["일관객"]
    .sum()
    .sort_values("날짜")
)


# 일관객 합계가 가장 큰 날짜 3개
top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("날짜")
)


fig3 = go.Figure()


# 영역 그래프
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


# TOP 3 표시
fig3.add_trace(
    go.Scatter(
        x=top3_days["날짜"],
        y=top3_days["일관객"],
        mode="markers+text",
        name="합계 TOP 3",
        text=[
            date.strftime("%Y년 %m월 %d일")
            for date in top3_days["날짜"]
        ],
        textposition="top center",
        marker=dict(size=10),
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


st.subheader("🏆 10위권 일관객 합계가 가장 컸던 날")

top3_display = (
    top3_days
    .sort_values(
        "일관객",
        ascending=False
    )
    .reset_index(drop=True)
)

for i, row in top3_display.iterrows():

    date_text = row["날짜"].strftime(
        "%Y년 %m월 %d일"
    )

    st.write(
        f"**{i + 1}위. {date_text}** — "
        f"10위권 일관객 합계: "
        f"{row['일관객']:,.0f}명"
    )


st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 내용을 직접 입력하세요.",
    placeholder="여기에 직접 입력하세요.",
    height=100,
    key="graph3_explanation"
)


# ==================================================
# 그래프 4
# ==================================================

st.divider()
st.header("📊 그래프 4. 영화별 기간 일관객 TOP 10")

st.write(
    "이 기간 동안 영화별 일관객을 모두 더해 "
    "관객수가 가장 많은 영화 10편을 비교합니다."
)


movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        top10_날수=("날짜", "nunique")
    )
    .reset_index()
)


top10_movies = (
    movie_summary
    .sort_values(
        "일관객합계",
        ascending=False
    )
    .head(10)
    .copy()
)


# 그래프에서는 작은 값부터 배치하여
# 큰 값이 위에 오도록 함
top10_graph = top10_movies.sort_values(
    "일관객합계",
    ascending=True
)


fig4 = px.bar(
    top10_graph,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="영화별 기간 일관객 TOP 10",
    labels={
        "일관객합계": "기간 일관객 합계",
        "영화명": "영화"
    },
    custom_data=["top10_날수"]
)


fig4.update_traces(
    hovertemplate=
    "영화: %{y}"
    "<br>기간 일관객 합계: %{x:,}명"
    "<br>10위권에 든 날수: %{customdata[0]}일"
    "<extra></extra>"
)


fig4.update_layout(
    xaxis_title="기간 일관객 합계",
    yaxis_title="영화",
    yaxis={
        "categoryorder": "total ascending"
    },
    hovermode="closest"
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


st.subheader("🏆 기간 일관객 TOP 10")

top10_table = (
    top10_movies
    .sort_values(
        "일관객합계",
        ascending=False
    )
    .reset_index(drop=True)
)

top10_table.index = (
    top10_table.index + 1
)

top10_table = top10_table.rename(
    columns={
        "영화명": "영화",
        "일관객합계": "기간 일관객 합계",
        "top10_날수": "10위권에 든 날수"
    }
)


top10_table["기간 일관객 합계"] = (
    top10_table["기간 일관객 합계"]
    .map(lambda x: f"{x:,.0f}명")
)

top10_table["10위권에 든 날수"] = (
    top10_table["10위권에 든 날수"]
    .map(lambda x: f"{x}일")
)


st.dataframe(
    top10_table,
    use_container_width=True
)


st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 내용을 직접 입력하세요.",
    placeholder="여기에 직접 입력하세요.",
    height=100,
    key="graph4_explanation"
)


# ==================================================
# 그래프 5
# ==================================================

st.divider()
st.header("📊 그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "날짜에서 월과 요일을 뽑아 "
    "월별·요일별 일관객 합계를 히트맵으로 보여줍니다."
)


# --------------------------------------------------
# 월과 요일 추출
# --------------------------------------------------

heatmap_df = df.copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month

# 월요일=0, 화요일=1, ..., 일요일=6
heatmap_df["요일번호"] = (
    heatmap_df["날짜"].dt.dayofweek
)

weekday_map = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
    5: "토요일",
    6: "일요일"
}

heatmap_df["요일"] = (
    heatmap_df["요일번호"]
    .map(weekday_map)
)


# --------------------------------------------------
# 월 × 요일별 일관객 합계 계산
# --------------------------------------------------

heatmap_data = (
    heatmap_df
    .groupby(
        ["월", "요일번호", "요일"],
        as_index=False
    )["일관객"]
    .sum()
    .sort_values(
        ["월", "요일번호"]
    )
)


# --------------------------------------------------
# 모든 월 × 요일 조합을 만들기
# --------------------------------------------------

all_months = range(1, 13)
all_weekdays = range(7)

all_combinations = pd.MultiIndex.from_product(
    [all_months, all_weekdays],
    names=["월", "요일번호"]
).to_frame(index=False)

all_combinations["요일"] = (
    all_combinations["요일번호"]
    .map(weekday_map)
)


heatmap_data = all_combinations.merge(
    heatmap_data[
        ["월", "요일번호", "일관객"]
    ],
    on=["월", "요일번호"],
    how="left"
)

heatmap_data["일관객"] = (
    heatmap_data["일관객"]
    .fillna(0)
)


# --------------------------------------------------
# 히트맵용 표 형태로 변환
# --------------------------------------------------

weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]


heatmap_pivot = heatmap_data.pivot(
    index="월",
    columns="요일",
    values="일관객"
)

heatmap_pivot = heatmap_pivot[
    weekday_order
]

heatmap_pivot = heatmap_pivot.reindex(
    range(1, 13)
)


# --------------------------------------------------
# 히트맵 생성
# --------------------------------------------------

fig5 = px.imshow(
    heatmap_pivot,
    x=weekday_order,
    y=[f"{month}월" for month in range(1, 13)],
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    },
    title="월 × 요일별 일관객 합계",
    text_auto=".3s",
    aspect="auto",
    color_continuous_scale="Blues"
)


fig5.update_traces(
    hovertemplate=
    "월: %{y}"
    "<br>요일: %{x}"
    "<br>일관객 합계: %{z:,}명"
    "<extra></extra>"
)


fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    coloraxis_colorbar_title="일관객 합계"
)


st.plotly_chart(
    fig5,
    use_container_width=True
)


# --------------------------------------------------
# 그래프 5 해석 입력
# --------------------------------------------------

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 내용을 직접 입력하세요.",
    placeholder="여기에 직접 입력하세요.",
    height=100,
    key="graph5_explanation"
)


# ==================================================
# 그래프 6 자리
# ==================================================

st.divider()
st.header("📊 그래프 6")
st.write("다음 그래프를 이곳에 추가할 수 있습니다.")

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프를 보고 알 수 있는 내용을 직접 입력하세요.",
    placeholder="여기에 직접 입력하세요.",
    height=100,
    key="graph6_explanation"
)
