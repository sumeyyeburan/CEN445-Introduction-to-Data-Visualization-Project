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

1. **Treemap — Region → Country Impact Visualization**  
   - Shows which regions and countries contribute most to the total impact.

2. **Parallel Coordinates Plot (PCP) — Multidimensional Incident Profiles**  
   - Displays year, month, region, attack type, target type, weapon type, and selected metrics together.

3. **Bubble Matrix — Attack Type × Target Type Interaction**  
   - Highlights which attack–target combinations generate the highest impact.

4. **Attack Composition Over Time (Area Chart)**  
   - Visualizes how the distribution of attack types evolves across years.

5. **Scatter Matrix (SPLOM) — Multivariate Analysis**  
   - Explores correlations and relationships between selected numeric variables.

6. **Calendar Heatmap — Year–Month Intensity**  
   - Shows which year–month combinations have the highest concentration of incidents.

7. **Density Map — Geographic Clustering of Incidents**  
   - Displays spatial concentration using a global density (heat) map.

8. **Violin Plot — Distribution of Impact by Attack Type**  
   - Shows the distribution (spread, median, density) of metric values for each attack type.

9. **Sunburst Chart — Region → Attack Type → Target Hierarchy**  
   - Visualizes hierarchical relationships between region, attack type, and target type.

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

* Sümeyye Buran: Preprocessing, Select Numeric Dimensions feature, Treemap, Parallel Coordinates, Bubble Matrix.
* Ayşe Gençalioğlu: Dataset research/selection, filters, multilingual support, Heatmap, Attack Composition, Scatter Plot.
* Fatma Nur Gençdoğan: Rule-based chatbot, Density Map, Violin Plot, Sunburst Chart.

---

