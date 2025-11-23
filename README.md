# 🌍 Global Terrorism Dashboard — README

An interactive data visualization dashboard built with **Python + Streamlit** for the *CEN445 Introduction to Data Visualization* course. It provides analytical insights into the Global Terrorism Database (GTD) using advanced visualization techniques and rich interactivity.

---

## 📌 1. Project Overview

This dashboard explores global terrorism incidents across decades using a set of advanced, interactive visualizations. Users can slice the data by year, country, region, and attack type, and examine multiple metrics such as fatalities, injuries, and combined casualties.

The project includes **9 advanced visualization modules**, multiple interactive filters, analytical summaries, and a built‑in chatbot assistant for quick insights.

---

## 📊 2. Dataset Information

* **Source:** Global Terrorism Database (preprocessed version)
* **File:** `gtd_insight_ready.csv`
* **Size:** 2,000+ rows and 7+ columns
* **Data Types:** Numerical, categorical, geographic
* **Preprocessing Applied:**

  * Missing value handling (median imputation)
  * Outlier filtering using Z-score
  * Numeric conversions
  * Feature engineering (`casualties`, `month_name`)

---

## 🛠️ 3. Technology Stack

* **Python 3.x**
* **Streamlit** (UI framework)
* **Pandas** (data manipulation)
* **Plotly Express / Graph Objects** (interactive visuals)
* **SciPy** (statistics & outlier detection)

---

## 📁 4. Project Structure

```
├── app.py                 # Main Streamlit application
├── gtd_insight_ready.csv  # Dataset
└── README.md              # Project description
```

---

## 🎨 5. Dashboard Features & Visualizations

This dashboard implements **9 distinct & advanced visualizations**:

1. **Density Map** — Geographic clustering of incidents
2. **Treemap** — Region → Country impact visualization
3. **Attack Composition Over Time** (Area chart)
4. **Scatter Matrix (SPLOM)** — Multivariate analysis
5. **Calendar Heatmap** — Year–Month intensity
6. **Violin Plot** — Monthly impact distributions
7. **Parallel Coordinates** — Multidimensional incident profiles
8. **Sunburst Chart** — Region → Attack Type → Target hierarchy
9. **Bubble Matrix** — Attack Type × Target Type interaction

Each module includes:

* Dynamic filtering
* Hover-based tooltips
* Zooming, panning, legend selection
* Automatically generated analytical summaries

---

## 🎛️ 6. Interactivity

The sidebar provides user-controlled filters:

* Year range slider
* Country selector
* Region selector
* Attack type selector
* Metric selectors for each visualization

All graphs update **instantly** to reflect active filters.

---

## 🤖 7. Analytical Chat Assistant

The dashboard includes a small built‑in chatbot that answers questions such as:

* "How many attacks occurred in 2010?"
* "Which country has the most incidents?"
* “What is the most dangerous country based on attack count?”

It uses pattern-based querying over the dataset.

---

## 🚀 8. Running the Project

### **1. Install Dependencies**

```bash
pip install streamlit pandas plotly scipy
```

### **2. Launch the Dashboard**

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser.

---

## 👥 9. Contributions

Add the names and roles of team members here.
Example:

* **Member A:** Data preprocessing, heatmap, SPLOM
* **Member B:** Density map, treemap, sunburst
* **Member C:** Dashboard layout, chatbot, report

---

