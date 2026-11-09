"""Local dashboard for the saved theLook monthly category export."""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from sales_analysis import DATA_PATH, category_summary, latest_month_comparison, load_sales, monthly_summary


st.set_page_config(page_title="E-commerce Sales Performance", layout="wide")
st.title("E-commerce Sales Performance")
st.caption("theLook BigQuery export · monthly product-category view · historical snapshot")

if not DATA_PATH.exists():
    st.error(f"Missing {DATA_PATH.name}. Place the saved export beside app.py.")
    st.stop()


@st.cache_data
def read_export(path: str, modified: float) -> pd.DataFrame:
    return load_sales(path)


sales = read_export(str(DATA_PATH), DATA_PATH.stat().st_mtime)
months = monthly_summary(sales)
categories = category_summary(sales)
latest = sales["month"].max()

st.info(
    f"This dashboard uses a saved export ending {latest:%B %Y}. The source is a synthetic public dataset, "
    "and its records may change when the BigQuery dataset is refreshed."
)

selected_category = st.selectbox("Product category", ["All categories", *sorted(sales["category"].unique())])
view = sales if selected_category == "All categories" else sales[sales["category"] == selected_category]
view_months = monthly_summary(view)

left, middle, right, last = st.columns(4)
left.metric("Recorded revenue", f"{view['revenue'].sum():,.2f}")
middle.metric("Items sold", f"{view['items_sold'].sum():,}")
right.metric("Category order occurrences", f"{view['total_orders'].sum():,}")
last.metric("Months with sales", f"{len(view_months):,}")
st.caption(
    "An order with items in two categories may be counted once in each category. "
    "Category order occurrences are not distinct storewide orders. Currency follows the source export."
)

st.subheader("Revenue over time")
st.line_chart(view_months, x="month", y="revenue", x_label="Month", y_label="Revenue")
if len(view_months) >= 2:
    previous, current = view_months.iloc[-2], view_months.iloc[-1]
    st.write(
        f"The latest recorded month is {current['month']:%B %Y}: revenue is "
        f"{current['revenue_change_pct']:+.1f}% from {previous['month']:%B %Y}. "
        "Treat a large change as a question to investigate, not proof of a campaign effect."
    )

st.subheader("Category performance")
if selected_category == "All categories":
    top = categories.head(10).sort_values("revenue")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(top["category"], top["revenue"], color="#316b9c")
    ax.set_xlabel("Recorded revenue")
    ax.set_ylabel("")
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)
    st.dataframe(
        categories[["category", "revenue", "revenue_share_pct", "items_sold", "category_order_occurrences"]]
        .style.format({"revenue": "{:,.2f}", "revenue_share_pct": "{:.1f}%"}),
        hide_index=True,
    )
else:
    st.write("Choose **All categories** to compare products across categories.")

st.subheader("Latest month by category")
changes = latest_month_comparison(sales)
st.write(f"Compare {latest:%B %Y} with {(latest - pd.DateOffset(months=1)):%B %Y}. A missing category in either month is treated as zero revenue for this comparison.")
st.dataframe(
    changes.style.format({
        "previous_month_revenue": "{:,.2f}",
        "latest_month_revenue": "{:,.2f}",
        "revenue_change": "{:+,.2f}",
        "change_pct": "{:+.1f}%",
    }, na_rep="n/a"),
    hide_index=True,
)
st.download_button(
    "Download monthly summary",
    months.to_csv(index=False).encode("utf-8"),
    file_name="monthly_sales_summary_rebuilt.csv",
    mime="text/csv",
)

st.caption(
    "Scope: the saved file contains only month and product category aggregates. "
    "It cannot answer customer, brand, location, profit, or distinct storewide order questions. "
    "The dashboard is descriptive, not a forecast."
)
