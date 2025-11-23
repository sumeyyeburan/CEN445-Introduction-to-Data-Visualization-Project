import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(page_title="GTD Dashboard - No Filters", layout="wide")

# -----------------------------
# LOAD & PREPROCESS DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("gtd_insight_ready.csv")
    df = df.copy()

    # Convert numeric fields
    num_cols = ["nkill", "nwound", "latitude", "longitude", "imonth"]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Keep valid months
    df = df[df["imonth"].between(1, 12)]

    # Fill missing numeric values using median
    for c in ["nkill", "nwound", "latitude", "longitude"]:
        df[c] = df[c].fillna(df[c].median())

    # Outlier detection with Z-score
    zscore_cols = ["nkill", "nwound", "latitude", "longitude"]
    z_scores = stats.zscore(df[zscore_cols], nan_policy='omit')
    z_df = pd.DataFrame(z_scores, columns=zscore_cols)

    df = df[(z_df.abs() < 4).all(axis=1)]

    # Feature engineering
    df["casualties"] = df["nkill"] + df["nwound"]
    df["month_name"] = pd.to_datetime(df["imonth"], format="%m").dt.strftime("%b")

    return df

df = load_data()

# -----------------------------
# KPI ROW
# -----------------------------
st.title(" Global Terrorism Dashboard")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Incidents", f"{len(df):,}")
kpi2.metric("Countries", df["country_txt"].nunique())
kpi3.metric("Attack Types", df["attacktype1_txt"].nunique())
kpi4.metric("Total Killed", f"{int(df['nkill'].sum()):,}")

# Helper function
def metric_from_dims(dataframe, dims):
    return dataframe[dims].sum(axis=1)

DEFAULT_DIMS = ["nkill", "nwound", "casualties"]

# =========================================================
# 1) TREEMAP
# =========================================================
st.subheader(" 1) Region → Country Treemap")
st.markdown("**Question:** Which regions and countries contribute most to the overall impact?")

tmp = df.copy()
tmp["metric_value"] = metric_from_dims(tmp, DEFAULT_DIMS)

tree = tmp.groupby(["region_txt", "country_txt"])["metric_value"].sum().reset_index()

fig1 = px.treemap(
    tree,
    path=["region_txt", "country_txt"],
    values="metric_value",
    color="region_txt",
    height=450
)
st.plotly_chart(fig1, use_container_width=True)

# =========================================================
# 2) PARALLEL COORDINATES
# =========================================================
st.subheader(" 2) Parallel Coordinates")
st.markdown("**Question:** How do incidents differ across year, month, region, attack type, target type, weapon type, and selected metrics?")

pcp = df.copy()
pcp["region_code"] = pcp["region_txt"].astype("category").cat.codes
pcp["attack_code"] = pcp["attacktype1_txt"].astype("category").cat.codes
pcp["target_code"] = pcp["targtype1_txt"].astype("category").cat.codes
pcp["weapon_code"] = pcp["weaptype1_txt"].astype("category").cat.codes

dimensions = [
    "iyear", "imonth", "region_code",
    "attack_code", "target_code", "weapon_code"
] + DEFAULT_DIMS

pcp_sample = pcp[dimensions].dropna().sample(5000, random_state=5)

fig2 = px.parallel_coordinates(
    pcp_sample,
    dimensions=dimensions,
    color="nkill",
    height=450
)

st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# 3) BUBBLE MATRIX
# =========================================================
st.subheader(" 3) Bubble Matrix — Attack × Target")
st.markdown("**Question:** Which attack type–target type combination produces the highest impact?")

tmp = df.copy()
tmp["metric_value"] = metric_from_dims(tmp, DEFAULT_DIMS)

bubble = tmp.groupby(["attacktype1_txt", "targtype1_txt"])["metric_value"].sum().reset_index()

fig3 = px.scatter(
    bubble,
    x="attacktype1_txt",
    y="targtype1_txt",
    size="metric_value",
    color="metric_value",
    color_continuous_scale="Viridis",
    height=560
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
st.success("Dashboard Loaded Successfully ✓")