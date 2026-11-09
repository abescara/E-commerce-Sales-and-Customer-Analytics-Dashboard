# E-commerce Sales Performance Analysis

An analysis of monthly product-category sales in a saved export from Google's synthetic `thelook_ecommerce` BigQuery dataset. It answers: How did recorded revenue change over time? Which categories contributed most? Which categories drove the latest month-to-month change?

## Repository contents

- `ecommerce_master.csv`: saved aggregated data, with 2,175 month-category rows from January 2019 through September 2026.
- `sales_analysis.py`: data checks and reusable monthly and category calculations.
- `sales_performance_analysis.ipynb`: documented analysis, with a title and short explanation before every code cell.
- `app.py`: interactive local Streamlit dashboard with a category filter and downloadable monthly summary.
- `monthly_category_sales.sql`: **proposed** BigQuery query for a new export. It has not been verified against the saved CSV; the original query and source snapshot are unavailable.
- `category_summary.csv`, `monthly_sales_summary.csv`, `kpi_summary.csv`: older derived exports. The Python analysis and dashboard define the current metrics.

## Data and metric definitions

Each source row is one **month and product category**. `revenue` is recorded sale value; `items_sold` is item count; `average_item_price` approximately equals revenue divided by items sold. `total_orders` counts orders **within a category**. Summing it across categories gives *category order occurrences*, not unique storewide orders: an order with items in two categories may be counted twice. The saved file has no order IDs, customer IDs, profit, brands, or location fields.

The data is synthetic and can change when the upstream dataset is regenerated. Results describe this saved snapshot; they do not establish causation or forecast future sales. Currency follows the source export; no conversion was performed.

## Run locally

Create a Python environment in the repository root, install `requirements.txt`, then run:

```powershell
python sales_analysis.py
streamlit run app.py
```

Open `sales_performance_analysis.ipynb` in VS Code or Jupyter and run cells from top to bottom. It reads the local CSV, so cloud credentials are unnecessary. To refresh from BigQuery, review the proposed SQL and record its run date and filters. An exact match with the historical CSV is not expected.

## Findings from the saved snapshot

- Recorded revenue totals **2,691,096.65** across 93 months and 26 categories.
- **Outerwear & Coats** leads recorded revenue at **325,754.89**, about **12.1%** of the total; **Jeans** follows at **314,198.92**.
- September 2026 recorded revenue is **210,289.22**, up **81.4%** from August. Investigate the underlying transactions and data generation before giving this jump a business explanation.

## Business use

The dashboard helps an analyst spot unusual months and choose categories to examine. A real business would reconcile transactions, inspect returns and margins, and check inventory or campaigns before changing promotions or purchasing.

## Source and scope

The `thelook_ecommerce` public dataset appears in [Google Cloud's public dataset documentation](https://docs.cloud.google.com/bigquery/public-data). Google describes theLook as synthetic in its [training lab](https://partner.skills.google/focuses/80989?parent=catalog). The repository's older notebook and exports predate this documented analysis. No Power BI `.pbix` file is included; the interactive deliverable is Streamlit.

## Author

Angel John B. Escara · BS Computer Science, Data Science specialization · FEU Institute of Technology
