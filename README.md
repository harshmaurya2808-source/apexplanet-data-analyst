# ApexPlanet Data Analytics Internship — 30-Day Project

End-to-end data analytics project completed as part of the ApexPlanet Software Data Analytics Internship,
using the Superstore Sales dataset.

## Project Structure
```
apexplanet-data-analyst/
├── data/                          # Raw and cleaned datasets
├── notebooks/
│   ├── eda.ipynb                  # Task 1: Data cleaning & exploratory analysis
│   ├── sql_integration.ipynb      # Task 2: SQL + Python/MySQL integration
│   ├── visualizations.ipynb       # Task 3: Python data visualizations
│   └── advanced_analytics.ipynb   # Task 4: Statistics, clustering, prediction
├── scripts/
│   ├── db_utils.py                # Reusable MySQL connection utility
│   ├── queries.sql                # SQL practice queries + business questions
│   └── pipeline.py                # Task 5: Automated ETL + KPI pipeline
├── dashboards/
│   └── superstore_dashboard.twbx  # Task 3: Tableau interactive dashboard
├── reports/
│   ├── charts/                    # Exported PNG/HTML visualizations
│   ├── superstore_kpi_report.xlsx # Automated KPI export
│   └── executive_summary.pdf      # Task 5: Final report
├── .github/workflows/
│   └── pipeline.yml               # Scheduled automation (GitHub Actions)
├── requirements.txt
└── README.md
```

## Tech Stack
- **Python:** pandas, numpy, matplotlib, seaborn, plotly, scipy, statsmodels, scikit-learn
- **Database:** MySQL, SQLAlchemy, PyMySQL
- **Visualization/BI:** Tableau Public
- **Automation:** GitHub Actions

## Task Summary
| Task | Description |
|---|---|
| 1 | Environment setup, data cleaning, exploratory data analysis |
| 2 | SQL fundamentals, advanced SQL (CTEs, window functions), Python-MySQL integration |
| 3 | Python visualizations + interactive Tableau dashboard |
| 4 | Hypothesis testing, time series decomposition, K-Means clustering, predictive modeling |
| 5 | Executive report, pipeline automation, final submission |

## Running the Automated Pipeline
```bash
pip install -r requirements.txt
python scripts/pipeline.py
```
This loads the raw dataset, cleans it, calculates KPIs, and exports everything to
`reports/superstore_kpi_report.xlsx`.

## Key Insights
See `reports/executive_summary.pdf` for the full write-up. Highlights:
- Technology category drives the highest total sales
- Sales show clear seasonality, peaking toward year-end
- Customer segmentation identified 4 distinct groups (VIP, at-risk, low-value, active frequent buyers)
- [Add your own top findings here]

## Author
Harsh — Data Analytics Intern, ApexPlanet Software Pvt. Ltd.
