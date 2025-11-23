import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

st.set_page_config(page_title="Mini Dashboard", layout="wide")

st.title(" Mini Global Terrorism Dashboard ")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("gtd_insight_ready.csv")
    df = df.copy()

    # Numeric columns
    num_cols = ["nkill", "nwound", "latitude", "longitude", "imonth"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df[df["imonth"].between(1, 12)]

    df["nkill"] = df["nkill"].fillna(df["nkill"].median())
    df["nwound"] = df["nwound"].fillna(df["nwound"].median())
    df["latitude"] = df["latitude"].fillna(df["latitude"].median())
    df["longitude"] = df["longitude"].fillna(df["longitude"].median())

    df["casualties"] = df["nkill"] + df["nwound"]
    df["month_name"] = pd.to_datetime(df["imonth"], format="%m").dt.strftime("%b")

    return df

df = load_data()

# =========================================================
# 7) DENSITY MAP
# =========================================================
st.header("7) Geographic Density Map")

tmp = df.copy()
tmp["metric_value"] = tmp["casualties"]

map_sample = tmp.sample(min(len(tmp), 15000), random_state=7)

fig7 = px.density_mapbox(
    map_sample,
    lat="latitude",
    lon="longitude",
    z="metric_value",
    radius=10,
    zoom=1.1,
    mapbox_style="open-street-map",
    height=450
)
st.plotly_chart(fig7, use_container_width=True)

# =========================================================
# 8) VIOLIN PLOT
# =========================================================
st.header("8) Violin Plot (Attack Type vs Casualties)")

tmp = df.copy()
tmp["metric_value"] = tmp["casualties"]

top_atks = (
    tmp.groupby("attacktype1_txt")["metric_value"].sum()
    .sort_values(ascending=False).head(8).index
)
vdf = tmp[tmp["attacktype1_txt"].isin(top_atks)]

fig8 = px.violin(
    vdf,
    x="attacktype1_txt",
    y="metric_value",
    box=True,
    points="outliers",
    height=450
)
st.plotly_chart(fig8, use_container_width=True)

# =========================================================
# 9) SUNBURST
# =========================================================
st.header("9) Sunburst Diagram (Region → Attack → Target)")

tmp = df.copy()
tmp["metric_value"] = tmp["casualties"]

sb = tmp.groupby(
    ["region_txt", "attacktype1_txt", "targtype1_txt"]
)["metric_value"].sum().reset_index()

fig9 = px.sunburst(
    sb,
    path=["region_txt", "attacktype1_txt", "targtype1_txt"],
    values="metric_value",
    height=450
)
st.plotly_chart(fig9, use_container_width=True)

# -------------------------------------------------
# CHATBOT — ANALYTIC ASSISTANT
# -------------------------------------------------
st.markdown("---")
st.header("Mini Analytical Chatbot")

def answer_question(question):
    q = question.lower().strip()
    import re

    # year question
    year_match = re.findall(r"19\\d{2}|20\\d{2}", q)
    if year_match:
        year = int(year_match[0])
        count = len(df[df["iyear"] == year])
        return f"In {year}, there were {count} incidents."

    # most attacks country
    if "country" in q and "most" in q:
        top_country = df["country_txt"].value_counts().idxmax()
        cnt = df["country_txt"].value_counts().max()
        return f"The country with the highest number of attacks is {top_country} ({cnt} incidents)."

    # deadliest year
    if "deadliest" in q or "fatalities" in q:
        dyear = df.groupby("iyear")["nkill"].sum().idxmax()
        kills = df.groupby("iyear")["nkill"].sum().max()
        return f"The deadliest year was {dyear} with {int(kills)} deaths."

    if "total attacks" in q:
        return f"The dataset contains {len(df):,} incidents."

    if "how many died" in q or "fatalities" in q:
        total_dead = int(df["nkill"].sum())
        total_wounded = int(df["nwound"].sum())
        return f"Total: {total_dead} dead, {total_wounded} wounded."

    if "attack types" in q:
        t = df["attacktype1_txt"].nunique()
        return f"There are {t} attack types."

    if "hello" in q:
        return "Hello! Ask me anything about the dataset."

    return (
        "I didn't understand. Try asking:\n"
        "- How many attacks occurred in 2015?\n"
        "- Which country has the most incidents?\n"
        "- What is the total number of fatalities?"
    )

user_q = st.text_input("Ask a question:")
if user_q:
    st.info(answer_question(user_q))
