import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(page_title="GTD Dashboard – Core Filters + Charts 4-5-6", layout="wide")

# -----------------------------
# LANGUAGE STRINGS
# -----------------------------
TEXT = {
    "tr": {
        "lang_label": "Dil / Language",
        "filters": "Filtreler",
        "year_range": "Yıl aralığı",
        "countries": "Ülkeler",
        "regions": "Bölgeler",
        "attack_types": "Saldırı türleri",
        "select_dims": "Sayısal metrik seç",
        "select_at_least_one": "En az bir metrik seçin.",

        "title": "🌍 Küresel Terörizm Dashboard",

        "c4": "📈 4) Zaman İçinde Saldırı Türü Kompozisyonu",
        "q4": "Soru: Zaman içinde saldırı türleri nasıl değişiyor?",

        "c5": "🧬 5) Çok Değişkenli Scatter Matrix (SPLOM)",
        "q5": "Soru: Seçilen sayısal değişkenler arasında ilişki var mı?",

        "c6": "📅 6) Yıl–Ay Heatmap",
        "q6": "Soru: Yıl–ay bazında en yoğun dönemler hangileri?",

        "ready": "Dashboard Hazır ✓",
    },

    "en": {
        "lang_label": "Language",
        "filters": "Filters",
        "year_range": "Year range",
        "countries": "Countries",
        "regions": "Regions",
        "attack_types": "Attack types",
        "select_dims": "Select numeric metrics",
        "select_at_least_one": "Select at least one metric.",

        "title": "🌍 Global Terrorism Dashboard",

        "c4": "📈 4) Attack Type Composition Over Time",
        "q4": "Question: How do attack types evolve over time?",

        "c5": "🧬 5) Multivariate Scatter Matrix (SPLOM)",
        "q5": "Question: How are selected numerical variables related?",

        "c6": "📅 6) Year–Month Heatmap",
        "q6": "Question: Which year–month periods show peak intensity?",

        "ready": "Dashboard Ready ✓",
    }
}

# -----------------------------
# SIDEBAR — LANGUAGE SELECTION
# -----------------------------
st.sidebar.title(" ")

lang = st.sidebar.selectbox(
    TEXT["en"]["lang_label"],
    ["tr", "en"],
    format_func=lambda x: "🇹🇷 Türkçe" if x == "tr" else "🇬🇧 English",
    key="lang_select"
)
T = TEXT[lang]

# -----------------------------
# LOAD & PREPROCESS DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("gtd_insight_ready.csv")
    df = df.copy()

    num_cols = ["nkill", "nwound", "latitude", "longitude", "imonth"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df[df["imonth"].between(1, 12)]

    for c in ["nkill", "nwound", "latitude", "longitude"]:
        df[c] = df[c].fillna(df[c].median())

    z_cols = ["nkill", "nwound", "latitude", "longitude"]
    z_scores = stats.zscore(df[z_cols], nan_policy="omit")
    z_df = pd.DataFrame(z_scores, columns=z_cols)
    df = df[(z_df.abs() < 4).all(axis=1)]

    df["casualties"] = df["nkill"] + df["nwound"]
    df["month_name"] = pd.to_datetime(df["imonth"], format="%m").dt.strftime("%b")

    return df

df = load_data()

NUM_COLS = ["nkill", "nwound", "casualties"]
DEFAULT_DIMS = ["nkill", "nwound", "casualties"]

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title(T["filters"])

year_min, year_max = int(df["iyear"].min()), int(df["iyear"].max())
year_range = st.sidebar.slider(
    T["year_range"], year_min, year_max, (year_min, year_max), key="year_range"
)

top_countries = df["country_txt"].value_counts().head(20).index.tolist()
countries = st.sidebar.multiselect(
    T["countries"], top_countries, default=top_countries, key="countries_filter"
)

regions = df[df["country_txt"].isin(top_countries)]["region_txt"].unique().tolist()
region_sel = st.sidebar.multiselect(
    T["regions"], regions, default=regions, key="regions_filter"
)

attack_types = sorted(df["attacktype1_txt"].unique())
attack_sel = st.sidebar.multiselect(
    T["attack_types"], attack_types, default=attack_types, key="attack_filter"
)

# -----------------------------
# APPLY FILTERS
# -----------------------------
df_f = df[
    (df["iyear"].between(year_range[0], year_range[1])) &
    (df["country_txt"].isin(countries)) &
    (df["region_txt"].isin(region_sel)) &
    (df["attacktype1_txt"].isin(attack_sel))
].copy()

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title(T["title"])

def metric_val(df, dims):
    return df[dims].sum(axis=1)


# =========================================================
# 4) ATTACK COMPOSITION OVER TIME
# =========================================================
st.subheader(T["c4"])
st.markdown(f"**{T['q4']}**")

dims_atk = DEFAULT_DIMS  # sabit dims

tmp = df_f.copy()
tmp["metric_value"] = metric_val(tmp, dims_atk)

atk_year = tmp.groupby(["iyear", "attacktype1_txt"])["metric_value"].sum().reset_index()

fig4 = px.area(
    atk_year,
    x="iyear",
    y="metric_value",
    color="attacktype1_txt",
    height=450
)

st.plotly_chart(fig4, use_container_width=True)

# =========================================================
# 5) SPLOM
# =========================================================
st.subheader(T["c5"])
st.markdown(f"**{T['q5']}**")

splom_cols = DEFAULT_DIMS

splom_sample = df_f[splom_cols + ["attacktype1_txt"]].dropna()
splom_sample = splom_sample.sample(min(len(splom_sample), 4000), random_state=11)

fig5 = px.scatter_matrix(
    splom_sample,
    dimensions=splom_cols,
    color="attacktype1_txt",
    height=550
)

fig5.update_layout(dragmode="select")
st.plotly_chart(fig5, use_container_width=True)

# =========================================================
# 6) YEAR–MONTH HEATMAP
# =========================================================
st.subheader(T["c6"])
st.markdown(f"**{T['q6']}**")

tmp = df_f.copy()
tmp["metric_value"] = metric_val(tmp, DEFAULT_DIMS)

month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

ym = tmp.groupby(["iyear", "month_name"])["metric_value"].sum().reset_index()
ym["month_name"] = pd.Categorical(ym["month_name"], categories=month_order, ordered=True)

pivot_ym = ym.pivot_table(index="month_name", columns="iyear", values="metric_value", fill_value=0)

fig6 = px.imshow(
    pivot_ym,
    aspect="auto",
    color_continuous_scale="Inferno",
    height=450
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.success(T["ready"])
