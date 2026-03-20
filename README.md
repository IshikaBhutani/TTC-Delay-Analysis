# 🚌 TTC Delay Analysis Dashboard (2023–2024)

**An end-to-end data analysis project** exploring delay patterns across Toronto's bus, subway, and streetcar network using open government data. Built to demonstrate data cleaning, exploratory analysis, and interactive dashboard development.

---

## 📌 Business Problem

Toronto's TTC serves over 1 million riders daily, yet delays remain a persistent pain point affecting commuter experience and operational efficiency. This project answers five key questions:

- Which routes experience the most delays?
- What time of day and day of week are worst for riders?
- What are the leading causes of delays?
- How does delay frequency differ across buses, subways, and streetcars?
- Are delays getting better or worse — 2023 vs 2024?

Answers to these questions give TTC operations teams, city planners, and commuters actionable insight into where the system is breaking down and why.

---

## 📂 Dataset

| Field | Detail |
|---|---|
| **Source** | [Open Data Toronto](https://open.toronto.ca) |
| **Datasets** | TTC Bus Delay Data, TTC Subway Delay Data, TTC Streetcar Delay Data |
| **Years** | 2023 and 2024 (6 files total) |
| **Raw Records** | ~194,000 rows across all files |
| **Cleaned Records** | 145,212 rows (after removing zeros and outliers) |
| **Format** | XLSX (downloaded), CSV (after cleaning) |
| **License** | Open Government Licence – Toronto |

**Columns used:** `Date`, `Route/Line`, `Time`, `Day`, `Location/Station`, `Incident`, `Min Delay`, `Direction`, `Vehicle`, `Transit Type`

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| **Python (pandas)** | Data cleaning and exploratory analysis |
| **HTML / Chart.js** | Interactive dashboard (no BI license required) |
| **Git / GitHub** | Version control and portfolio hosting |

---

## 🗂️ Project Structure

```
ttc-delay-analysis/
│
├── data/
│   ├── raw/                          ← Original .xlsx files from Open Toronto
│   │   ├── ttc-bus-delay-data-2023.xlsx
│   │   ├── ttc-bus-delay-data-2024.xlsx
│   │   ├── ttc-subway-delay-data-2023.xlsx
│   │   ├── ttc-subway-delay-data-2024.xlsx
│   │   ├── ttc-streetcar-delay-data-2023.xlsx
│   │   └── ttc-streetcar-delay-data-2024.xlsx
│   └── clean/
│       ├── bus_clean.csv
│       ├── subway_clean.csv
│       ├── streetcar_clean.csv
│       └── ttc_all_clean.csv         ← Master file used for dashboard
│
├── notebooks/
│   └── ttc_analysis.ipynb            ← Full cleaning + analysis walkthrough
│
├── dashboard/
│   └── ttc_dashboard.html            ← Interactive dashboard (open in browser)
│
├── screenshot.png                    ← Dashboard preview image
└── README.md
```

---

## ⚙️ How to Run

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/ttc-delay-analysis.git
cd ttc-delay-analysis
```

### 2. Install dependencies
```bash
pip install pandas openpyxl
```

### 3. Run the cleaning script
```bash
python notebooks/clean_data.py
```
This reads the 6 raw `.xlsx` files and outputs cleaned CSVs to `data/clean/`.

### 4. View the dashboard
Open `dashboard/ttc_dashboard.html` in any modern browser. No server needed — it runs entirely client-side.

---

## 🔍 Approach

### Data Cleaning
- Standardized column names across all 3 transit types (bus, subway, streetcar used different naming conventions)
- Parsed date/time strings into structured `hour`, `day_of_week`, `month` columns
- Removed records with `Min Delay = 0` (no actual delay occurred)
- Removed outliers above 300 minutes (likely data entry errors — 5+ hour delays on a single vehicle)
- Dropped nulls only on critical columns (`route`, `incident`, `min_delay`) to preserve as many rows as possible
- Added `transit_type` and `year` labels to enable cross-mode and year-over-year filtering

### Analysis
Grouped and aggregated data to answer each business question:
- **Route frequency:** `groupby('route').size()` → top 10 ranked by incident count
- **Time patterns:** `groupby('hour')['min_delay'].mean()` → average delay per hour
- **Day patterns:** `groupby('day_of_week').size()` → total incidents per day
- **Causes:** `groupby('incident').size()` → top 10 incident types
- **Trend:** `groupby(['year','month']).size()` → monthly comparison

---

## 📊 Key Findings

- 🚇 **YU (Yonge-University) subway line had the most delays** of any single route — 10,293 incidents — 60% more than the next highest route (BD line at 6,424). High ridership and line length make it especially vulnerable.

- 🔧 **Mechanical failure is the #1 cause of delays**, accounting for 28.6% of all incidents (41,482 events). This points to fleet maintenance as the single highest-leverage operational improvement area.

- 🌙 **Late-night hours (2–4 AM) have the longest average delay durations** — 28 to 32 minutes — more than double the peak-hour average of ~15 minutes. Reduced crew availability and fewer backup vehicles likely explain this.

- 📅 **Friday is the worst day** for delay frequency with 22,975 incidents. Midweek (Wednesday–Thursday) is nearly as bad. Sundays have the fewest delays at 15,842.

- 🚌 **Buses account for 71% of all delay incidents** (103,452 of 145,212), making it the highest-priority mode for operational improvements despite subways generating the most attention.

- 📈 **2024 saw more delays than 2023 in the first half of the year** (January–June average: +7.4% YoY), while 2023 had notably more incidents in Q4 (October–December). This seasonal divergence warrants further investigation.

---

## 💡 Recommendations

Based on the analysis, three targeted improvements could reduce delay frequency meaningfully:

1. **Prioritize YU and BD subway line maintenance windows** — given their outsized contribution to total delay count, targeted investment in track, signal, and rolling stock maintenance on these lines would have the highest system-wide impact.

2. **Accelerate mechanical inspection cycles for the bus fleet** — mechanical issues cause nearly 1 in 3 delays. A shift from reactive to preventive maintenance scheduling, particularly for high-frequency routes like 32, 36, and 52, could reduce this substantially.

3. **Increase overnight spare vehicle and crew coverage** — late-night delays are disproportionately long. Pre-positioning spare buses and operators at key overnight terminals (especially on Friday–Saturday nights) would reduce average delay duration during these windows.

---

## 📸 Dashboard Preview

![TTC Delay Analysis Dashboard](screenshot.png)

*Interactive dashboard with filters by transit type, year, and day of week.*

---

## 👤 Author

**Ishika Bhutani**
Data Analyst | Toronto, ON
[GitHub](https://github.com/yourusername) · [LinkedIn](https://linkedin.com/in/yourprofile)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).
Data sourced under the [Open Government Licence – Toronto](https://open.toronto.ca/open-data-license/).
