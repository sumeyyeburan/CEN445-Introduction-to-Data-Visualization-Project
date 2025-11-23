import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(page_title="GTD Dashboard", layout="wide")

st.markdown("""
<style>
body { background-color: #0f1117; }
.block-container { padding-top: 1rem; padding-bottom: 1rem; }
h2 { margin-top: 40px; }
.card {
    background: #111827;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 0 25px rgba(0,0,0,0.5);
    margin-bottom: 40px;
}
</style>
""", unsafe_allow_html=True)

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

    # imonth valid range
    df = df[df["imonth"].between(1, 12)]

    # Fill missing numeric values with median
    for c in ["nkill", "nwound", "latitude", "longitude"]:
        df[c] = df[c].fillna(df[c].median())

    # Outlier Detection (Z-score)
    zscore_cols = ["nkill", "nwound", "latitude", "longitude"]
    z_scores = stats.zscore(df[zscore_cols], nan_policy='omit')
    z_df = pd.DataFrame(z_scores, columns=zscore_cols)

    # keep only rows where |z| < 4
    mask = (z_df.abs() < 4).all(axis=1)
    df = df[mask]

    # Feature engineering
    df["casualties"] = df["nkill"] + df["nwound"]
    df["month_name"] = pd.to_datetime(df["imonth"], format="%m").dt.strftime("%b")

    return df

df = load_data()

NUM_COLS = ["nkill", "nwound", "casualties", "latitude", "longitude"]
DEFAULT_DIMS = ["nkill", "nwound", "casualties"]

# -----------------------------
# LANGUAGE STRINGS (RENUBMERED)
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
        "select_at_least_one": "En az bir sayısal metrik seç.",
        "select_at_least_two": "Lütfen en az iki sayısal metrik seç.",
        "title": " Küresel Terörizm Dashboard",
        "k_incidents": "Olay Sayısı",
        "k_countries": "Ülke Sayısı",
        "k_attack_types": "Saldırı Türü",
        "k_killed": "Toplam Ölü",
        "ready": "Dashboard Hazır ✓",

        # NEW ORDER / NEW NUMBERS
        "c1": " 1) Bölge → Ülke Treemap",
        "q1": "Soru: Hangi bölge ve ülkeler toplam etkiyi en çok oluşturuyor?",
       

        "c2": " 2) Paralel Koordinatlar",
        "q2": "Soru: Çok boyutlu olarak olay profilleri (yıl, ay, bölge, saldırı, hedef, silah ve metrikler) nasıl ayrışıyor?",
        

        "c3": " 3) Bubble Matrix — Saldırı × Hedef",
        "q3": "Soru: Hangi saldırı türü hangi hedef türünde en yoğun/ölümcül etkiyi yaratıyor?",
       

        "c4": " 4) Zaman İçinde Saldırı Türü Kompozisyonu",
        "q4": "Soru: Zaman içinde saldırı türleri nasıl değişiyor, hangi yıl/saldırı türü zirvede?",
       

        "c5": " 5) Çok Değişkenli Scatter Matrix (SPLOM)",
        "q5": "Soru: Seçilen sayısal değişkenler arasında nasıl ilişkiler var? (örn. ölü–yaralı korelasyonu)",
        

        "c6": " 6) Yıl–Ay Heatmap",
        "q6": "Soru: Yıl–ay bazında en yoğun dönemler hangileri? (mevsimsellik / pik aylar)",
        

        "c7": " 7) Olay Yoğunluğu Haritası",
        "q7": "Soru: Filtrelere göre olaylar coğrafi olarak en çok nerede yoğunlaşıyor?",
       

        "c8": " 8) Violin Plot — Saldırı Türüne Göre Dağılım",
        "q8": "Soru: Seçilen etki metriği saldırı türlerine göre nasıl dağılıyor? Hangi saldırı türü tipik olarak daha yüksek etki üretiyor?",
       

        "c9": " 9) Sunburst — Bölge → Saldırı → Hedef",
        "q9": "Soru: Bölge → saldırı türü → hedef türü hiyerarşisinde en baskın akış hangisi?",
        
    },

    "en": {
        "lang_label": "Language",
        "filters": "Filters",
        "year_range": "Year range",
        "countries": "Countries",
        "regions": "Regions",
        "attack_types": "Attack types",
        "select_dims": "Select numeric dimensions",
        "select_at_least_one": "Select at least one numeric dimension.",
        "select_at_least_two": "Please select at least two numeric dimensions.",
        "title": " Global Terrorism Dashboard",
        "k_incidents": "Incidents",
        "k_countries": "Countries",
        "k_attack_types": "Attack Types",
        "k_killed": "Total Killed",
        "ready": "Dashboard Ready ✓",

        # NEW ORDER / NEW NUMBERS
        "c1": "1) Region → Country Treemap",
        "q1": "Question: Which regions and countries contribute most to the overall impact?",
        

        "c2": " 2) Parallel Coordinates",
        "q2": "Question: How do incidents differ multidimensionally across year, month, region, attack type, target type, weapon type, and selected metrics?",
       

        "c3": " 3) Bubble Matrix — Attack × Target",
        "q3": "Question: Which attack type–target type combination produces the highest impact?",
        

        "c4": " 4) Attack Type Composition Over Time",
        "q4": "Question: How do attack types evolve over time? Which year/attack type reaches the peak?",
       

        "c5": " 5) Multivariate Scatter Matrix (SPLOM)",
        "q5": "Question: What are the relationships between the selected numeric variables? (e.g., kill–wound correlation)",
        

        "c6": " 6) Year–Month Heatmap",
        "q6": "Question: Which year–month combinations show the highest intensity? Any seasonal peaks?",
        

        "c7": " 7) Geographic Density of Incidents",
        "q7": "Question: According to the filters, where are the incidents geographically concentrated the most?",
        
        
        "c8": " 8) Violin Plot — Distribution by Attack Type",
        "q8": "Question: How does the selected impact metric distribute across attack types? Which type typically yields higher impact?",
       

        "c9": " 9) Sunburst — Region → Attack → Target",
        "q9": "Question: In the hierarchy Region → Attack Type → Target Type, which flow dominates the most?",
       
    }
}

# -----------------------------
# SIDEBAR FILTERS + LANGUAGE
# -----------------------------
st.sidebar.title(" ")

lang = st.sidebar.selectbox(
    TEXT["en"]["lang_label"],
    ["tr", "en"],
    format_func=lambda x: "🇹🇷 Türkçe" if x == "tr" else "🇬🇧 English",
    key="lang_select"
)
T = TEXT[lang]

st.sidebar.title(T["filters"])

year_min, year_max = int(df["iyear"].min()), int(df["iyear"].max())
year_range = st.sidebar.slider(
    T["year_range"], year_min, year_max,
    (year_min, year_max), key="year_range"
)

remove_list = ["Philippines", "Thailand"]
top15 = (
    df[~df["country_txt"].isin(remove_list)]
    ["country_txt"].value_counts().head(15).index.tolist()
)

countries = st.sidebar.multiselect(
    T["countries"], top15,
    default=top15, key="countries_filter"
)

regions = df[df["country_txt"].isin(top15)]["region_txt"].unique().tolist()
region_sel = st.sidebar.multiselect(
    T["regions"], regions,
    default=regions, key="regions_filter"
)

attack_types = sorted(df["attacktype1_txt"].unique())
attack_sel = st.sidebar.multiselect(
    T["attack_types"], attack_types,
    default=attack_types, key="attack_filter"
)

# -----------------------------
# APPLY FILTERS
# -----------------------------
df_f = df.copy()
df_f = df_f[(df_f["iyear"] >= year_range[0]) & (df_f["iyear"] <= year_range[1])]
df_f = df_f[df_f["country_txt"].isin(countries)]
df_f = df_f[df_f["region_txt"].isin(region_sel)]
df_f = df_f[df_f["attacktype1_txt"].isin(attack_sel)]

# -----------------------------
# KPI ROW
# -----------------------------
st.title(T["title"])

k1, k2, k3, k4 = st.columns(4)
k1.metric(T["k_incidents"], f"{len(df_f):,}")
k2.metric(T["k_countries"], df_f["country_txt"].nunique())
k3.metric(T["k_attack_types"], df_f["attacktype1_txt"].nunique())
k4.metric(T["k_killed"], f"{int(df_f['nkill'].sum()):,}")

def metric_from_dims(dataframe, dims):
    return dataframe[dims].sum(axis=1)

# =========================================================
# 1) TREEMAP 
# =========================================================
with st.container():
    st.subheader(T["c1"])
    st.markdown(f"**{T['q1']}**")

    dims_tree = st.multiselect(
        T["select_dims"],
        NUM_COLS,
        default=DEFAULT_DIMS,
        key="dims_tree"
    )

    if len(dims_tree) == 0:
        st.info(T["select_at_least_one"])
    else:
        tmp = df_f.copy()
        tmp["metric_value"] = metric_from_dims(tmp, dims_tree)

        top_region = tmp.groupby("region_txt")["metric_value"].sum().sort_values(ascending=False).head(1)
        top_country = tmp.groupby("country_txt")["metric_value"].sum().sort_values(ascending=False).head(1)
        if len(top_region) and len(top_country):
            pass

        tree = tmp.groupby(["region_txt", "country_txt"])["metric_value"].sum().reset_index()
        fig1 = px.treemap(
            tree,
            path=["region_txt", "country_txt"],
            values="metric_value",
            color="region_txt",
            color_discrete_sequence=px.colors.qualitative.Set3,
            height=450
        )
        st.plotly_chart(fig1, use_container_width=True)

# =========================================================
# 2) PARALLEL COORDINATES
# =========================================================
with st.container():
    st.subheader(T["c2"])
    st.markdown(f"**{T['q2']}**")

    dims_par = st.multiselect(
        T["select_dims"],
        NUM_COLS,
        default=DEFAULT_DIMS,
        key="dims_par"
    )

    if len(dims_par) == 0:
        st.info(T["select_at_least_one"])
    else:
        pcp = df_f.copy()
        pcp["region_code"] = pcp["region_txt"].astype("category").cat.codes
        pcp["attack_code"] = pcp["attacktype1_txt"].astype("category").cat.codes
        pcp["target_code"] = pcp["targtype1_txt"].astype("category").cat.codes
        pcp["weapon_code"] = pcp["weaptype1_txt"].astype("category").cat.codes

        base_dims = ["iyear", "imonth", "region_code",
                     "attack_code", "target_code", "weapon_code"]
        used_dims = base_dims + dims_par

        pcp["metric_value"] = metric_from_dims(pcp, dims_par)

        pcp_s = pcp[used_dims + ["metric_value"]].dropna().sample(
            min(len(pcp), 5000), random_state=5
        )

        fig2 = px.parallel_coordinates(
            pcp_s, dimensions=used_dims,
            color="metric_value", height=450
        )

        label_map = {
            "iyear": "year",
            "imonth": "month",
            "region_code": "region",
            "attack_code": "attack",
            "target_code": "target",
            "weapon_code": "weapon"
        }
        for dim in fig2.data[0]["dimensions"]:
            if dim["label"] in label_map:
                dim["label"] = label_map[dim["label"]]

        fig2.update_layout(
            font=dict(size=14),
            margin=dict(l=40, r=40, t=40, b=40)
        )

        st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# 3) BUBBLE MATRIX
# =========================================================
with st.container():
    st.subheader(T["c3"])
    st.markdown(f"**{T['q3']}**")

    bubble_dims = st.multiselect(
        T["select_dims"],
        NUM_COLS,
        default=DEFAULT_DIMS,
        key="dims_bubble"
    )

    if len(bubble_dims) == 0:
        st.info(T["select_at_least_one"])
    else:
        tmp = df_f.copy()
        tmp["metric_value"] = metric_from_dims(tmp, bubble_dims)

        bubble = tmp.groupby(
            ["attacktype1_txt", "targtype1_txt"]
        )["metric_value"].sum().reset_index()

        if len(bubble):
            top_pair = bubble.sort_values("metric_value", ascending=False).iloc[0]
            

        fig3 = px.scatter(
            bubble,
            x="attacktype1_txt",
            y="targtype1_txt",
            size="metric_value",
            color="metric_value",
            color_continuous_scale="Viridis",
            height=560
        )

        fig3.update_layout(
            title="Bubble Matrix (weighted by selected numeric dimensions)" if lang == "en"
            else "Bubble Matrix (seçilen sayısal metriklerle ağırlıklı)",
            xaxis_title="Attack Type" if lang == "en" else "Saldırı Türü",
            yaxis_title="Target Type" if lang == "en" else "Hedef Türü"
        )

        st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# 4) ATTACK COMPOSITION OVER TIME
# =========================================================
with st.container():
    st.subheader(T["c4"])
    st.markdown(f"**{T['q4']}**")

    dims_atk = st.multiselect(
        T["select_dims"],
        NUM_COLS,
        default=DEFAULT_DIMS,
        key="dims_atk"
    )

    if len(dims_atk) == 0:
        st.info(T["select_at_least_one"])
    else:
        tmp = df_f.copy()
        tmp["metric_value"] = metric_from_dims(tmp, dims_atk)
        
        atk_year = tmp.groupby(["iyear", "attacktype1_txt"])["metric_value"].sum().reset_index()
        if len(atk_year):
            peak_row = atk_year.sort_values("metric_value", ascending=False).iloc[0]
            

        fig4 = px.area(
            atk_year, x="iyear", y="metric_value",
            color="attacktype1_txt", height=450
        )
        st.plotly_chart(fig4, use_container_width=True)

# =========================================================
# 5) SPLOM 
# =========================================================
with st.container():
    st.subheader(T["c5"])
    st.markdown(f"**{T['q5']}**")

    splom_cols = st.multiselect(
        T["select_dims"],
        NUM_COLS,
        default=DEFAULT_DIMS,
        key="dims_splom"
    )

    if len(splom_cols) >= 2:
        splom_sample = df_f[splom_cols + ["attacktype1_txt"]].dropna()
        splom_sample = splom_sample.sample(min(len(splom_sample), 4000), random_state=11)

        corr = splom_sample[splom_cols].corr(numeric_only=True)
        c_pairs = corr.abs().unstack().sort_values(ascending=False)
        c_pairs = c_pairs[c_pairs.index.get_level_values(0) != c_pairs.index.get_level_values(1)]
        if len(c_pairs):
            (a, b) = c_pairs.index[0]
            

        fig5 = px.scatter_matrix(
            splom_sample, dimensions=splom_cols,
            color="attacktype1_txt", height=550
        )
        fig5.update_layout(dragmode="select")
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info(T["select_at_least_two"])

# =========================================================
# 6) YEAR–MONTH HEATMAP 
# =========================================================
with st.container():
    st.subheader(T["c6"])
    st.markdown(f"**{T['q6']}**")

    dims_heat = st.multiselect(
        T["select_dims"],
        NUM_COLS,
        default=DEFAULT_DIMS,
        key="dims_heat"
    )

    if len(dims_heat) == 0:
        st.info(T["select_at_least_one"])
    else:

        month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                       "Jul","Aug","Sep","Oct","Nov","Dec"]

        tmp = df_f.copy()
        tmp["metric_value"] = metric_from_dims(tmp, dims_heat)

        ym = tmp.groupby(["iyear", "month_name"])["metric_value"].sum().reset_index()
        ym["month_name"] = pd.Categorical(ym["month_name"], categories=month_order, ordered=True)

        if len(ym):
            peak = ym.sort_values("metric_value", ascending=False).iloc[0]
            

        pivot_ym = ym.pivot_table(index="month_name", columns="iyear",
                                  values="metric_value", fill_value=0)

        fig6 = px.imshow(
            pivot_ym, aspect="auto",
            color_continuous_scale="Inferno", height=450
        )
        st.plotly_chart(fig6, use_container_width=True)

# =========================================================
# 7) DENSITY MAP
# =========================================================
with st.container():
    st.subheader(T["c7"])
    st.markdown(f"**{T['q7']}**")

    dims_map = st.multiselect(
        T["select_dims"],
        NUM_COLS,
        default=DEFAULT_DIMS,
        key="dims_map"
    )

    if len(dims_map) == 0:
        st.info(T["select_at_least_one"])
    else:
        tmp = df_f.copy()
        tmp["metric_value"] = metric_from_dims(tmp, dims_map)

        top_c = tmp.groupby("country_txt")["metric_value"].sum().sort_values(ascending=False).head(3)
        if len(top_c) > 0:
            pass

        map_sample = tmp.sample(min(len(tmp), 15000), random_state=7)
        fig7 = px.density_mapbox(
            map_sample,
            lat="latitude", lon="longitude",
            z="metric_value",
            radius=10,
            zoom=1.2, center=dict(lat=20, lon=0),
            mapbox_style="open-street-map",
            hover_data=["country_txt", "attacktype1_txt", "metric_value"],
            height=450
        )
        st.plotly_chart(fig7, use_container_width=True)

# =========================================================
# 8) VIOLIN PLOT
# =========================================================
with st.container():
    st.subheader(T["c8"])
    st.markdown(f"**{T['q8']}**")

    dims_violin = st.multiselect(
        T["select_dims"],
        NUM_COLS,
        default=DEFAULT_DIMS,
        key="dims_violin"
    )

    if len(dims_violin) == 0:
        st.info(T["select_at_least_one"])
    else:
        tmp = df_f.copy()
        tmp["metric_value"] = metric_from_dims(tmp, dims_violin)

        # to reduce clutter: keep top 8 attack types by total metric
        top_atks = (
            tmp.groupby("attacktype1_txt")["metric_value"].sum()
            .sort_values(ascending=False).head(8).index
        )
        vdf = tmp[tmp["attacktype1_txt"].isin(top_atks)]

        # answer: highest median attack type
        medians = vdf.groupby("attacktype1_txt")["metric_value"].median().sort_values(ascending=False)
        if len(medians):
            pass

        fig8 = px.violin(
            vdf,
            x="attacktype1_txt",
            y="metric_value",
            box=True,
            points="outliers",
            height=450
        )
        fig8.update_traces(
            marker_color="rgba(200,200,200,0.6)",
            line_color="rgba(200,200,200,1)"
        )
        st.plotly_chart(fig8, use_container_width=True)

# =========================================================
# 9) SUNBURST
# =========================================================
with st.container():
    st.subheader(T["c9"])
    st.markdown(f"**{T['q9']}**")

    dims_sun = st.multiselect(
        T["select_dims"],
        NUM_COLS,
        default=DEFAULT_DIMS,
        key="dims_sun"
    )

    if len(dims_sun) == 0:
        st.info(T["select_at_least_one"])
    else:
        tmp = df_f.copy()
        tmp["metric_value"] = metric_from_dims(tmp, dims_sun)

        sb = tmp.groupby(
            ["region_txt", "attacktype1_txt", "targtype1_txt"]
        )["metric_value"].sum().reset_index()

        if len(sb):
            top_path = sb.sort_values("metric_value", ascending=False).iloc[0]
            

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
st.header("💬 Analytical Chat Assistant")

def answer_question(question):
    q = question.lower().strip()
    import re

    year_match = re.findall(r"19\d{2}|20\d{2}", q)
    if year_match:
        year = int(year_match[0])
        count = len(df[df["iyear"] == year])
        return f"In {year}, a total of {count} incidents were recorded."

    if ("most" in q and "country" in q) or ("highest" in q and "country" in q):
        top_country = df["country_txt"].value_counts().idxmax()
        count = df["country_txt"].value_counts().max()
        return f"The country with the highest number of attacks is {top_country} ({count} incidents)."

    if "deadliest" in q or "most deaths" in q or "highest fatalities" in q:
        deadly_year = df.groupby("iyear")["nkill"].sum().idxmax()
        kills = df.groupby("iyear")["nkill"].sum().max()
        return f"The deadliest year was {deadly_year} with a total of {int(kills)} fatalities."

    if "total attacks" in q or "how many attacks" in q or "number of attacks" in q:
        return f"The dataset contains a total of {len(df):,} incidents."

    if "how many died" in q or "fatalities" in q or "death count" in q:
        total_dead = int(df["nkill"].sum())
        total_wounded = int(df["nwound"].sum())
        return (
            f"There were a total of {total_dead} fatalities "
            f"and {total_wounded} injuries recorded in the dataset."
        )

    if "attack types" in q or "types of attacks" in q:
        types_count = df["attacktype1_txt"].nunique()
        return f"The dataset includes {types_count} different types of attacks."

    if "hello" in q or "hi" in q:
        return "Hello. I can answer analytical questions about the terrorism dataset."

    return (
        "I could not clearly understand your question. You may ask things like:\n"
        "- How many attacks occurred in 2015?\n"
        "- Which country has the most incidents?\n"
        "- What is the total number of fatalities?\n"
        "- How many attack types exist?"
    )

user_q = st.text_input("Ask a question:")
if user_q:
    st.write("**Answer:**")
    st.info(answer_question(user_q))

# -----------------------------
# Footer
# -----------------------------
st.success(T["ready"])
