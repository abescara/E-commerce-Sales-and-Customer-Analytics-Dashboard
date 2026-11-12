# Data guide

This guide explains the saved `ecommerce_master.csv` used by the notebook, dashboard, and preview chart.

## Grain and coverage

One row represents **one product category in one month**. The file contains 2,175 rows, 26 categories, and 93 months from January 2019 through September 2026. Some early months have fewer than 26 category rows; a missing row does not prove zero sales.

## Columns

| Column | Meaning |
| --- | --- |
| `month` | First day of the reporting month |
| `category` | Product category name |
| `total_orders` | Distinct orders counted **within this category and month** |
| `items_sold` | Number of recorded sold items in this category and month |
| `revenue` | Sum of recorded sale prices for those items, in source currency |
| `average_item_price` | Approximate `revenue / items_sold`, rounded in the export |

## How to read the numbers

- Revenue and items can be summed across categories for a month.
- `total_orders` can be summed only if labeled **category order occurrences**. An order containing items from multiple categories can appear in more than one category count.
- The file has no transaction or customer identifiers, so it cannot support a unique storewide order count, customer retention, or customer-level analysis.
- Revenue is not profit. The file has no costs, returns, refunds, or marketing spend.
- The latest monthly jump is a pattern to investigate, not proof of a cause.

## Reproducing the preview

Run `python generate_preview.py` from the repository root after installing `requirements.txt`. The script reads the checked-in CSV and writes `assets/sales_preview.png`. The shorter chart label “Hoodies & Sweatshirts” stands for the full CSV category “Fashion Hoodies & Sweatshirts.”

The upstream theLook dataset is synthetic. The saved CSV is a historical snapshot; `monthly_category_sales.sql` is a proposed query for a new export and has not been verified to recreate it exactly.
