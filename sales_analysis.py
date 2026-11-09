"""Validate and summarize the saved theLook monthly category export."""

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "month", "category", "total_orders", "items_sold", "revenue", "average_item_price"
}
DATA_PATH = Path(__file__).parent / "ecommerce_master.csv"


def load_sales(path: str | Path = DATA_PATH) -> pd.DataFrame:
    """Read the monthly category table and reject malformed exports."""
    sales = pd.read_csv(path, parse_dates=["month"])
    missing = REQUIRED_COLUMNS - set(sales.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if sales[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("The export contains missing values in required columns")
    if sales.duplicated(["month", "category"]).any():
        raise ValueError("The export contains duplicate month-category rows")
    if not sales["month"].dt.is_month_start.all():
        raise ValueError("The month column must contain the first day of each month")
    if (sales[["total_orders", "items_sold", "revenue", "average_item_price"]] <= 0).any().any():
        raise ValueError("Counts, revenue, and average price must be positive")
    if (sales["items_sold"] < sales["total_orders"]).any():
        raise ValueError("Items sold cannot be lower than category order occurrences")
    if ((sales["revenue"] / sales["items_sold"] - sales["average_item_price"]).abs() > .02).any():
        raise ValueError("Average item price disagrees with revenue divided by items sold")
    return sales.sort_values(["month", "category"]).reset_index(drop=True)


def monthly_summary(sales: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue and item counts across categories by month."""
    monthly = sales.groupby("month", as_index=False).agg(
        revenue=("revenue", "sum"),
        category_order_occurrences=("total_orders", "sum"),
        items_sold=("items_sold", "sum"),
    )
    monthly["revenue_change_pct"] = monthly["revenue"].pct_change() * 100
    return monthly


def category_summary(sales: pd.DataFrame) -> pd.DataFrame:
    """Aggregate category totals without claiming distinct storewide orders."""
    category = sales.groupby("category", as_index=False).agg(
        revenue=("revenue", "sum"),
        category_order_occurrences=("total_orders", "sum"),
        items_sold=("items_sold", "sum"),
    )
    category["revenue_share_pct"] = category["revenue"] / category["revenue"].sum() * 100
    category["revenue_per_category_order"] = category["revenue"] / category["category_order_occurrences"]
    return category.sort_values("revenue", ascending=False).reset_index(drop=True)


def latest_month_comparison(sales: pd.DataFrame) -> pd.DataFrame:
    """Compare category revenue in the latest month with the preceding month."""
    latest = sales["month"].max()
    previous = latest - pd.DateOffset(months=1)
    compared = sales[sales["month"].isin([previous, latest])].pivot(
        index="category", columns="month", values="revenue"
    )
    compared = compared.reindex(columns=[previous, latest]).fillna(0)
    compared.columns = ["previous_month_revenue", "latest_month_revenue"]
    compared["revenue_change"] = compared["latest_month_revenue"] - compared["previous_month_revenue"]
    compared["change_pct"] = (
        compared["revenue_change"] / compared["previous_month_revenue"].replace(0, float("nan")) * 100
    )
    return compared.reset_index().sort_values("revenue_change", ascending=False)


def main() -> None:
    sales = load_sales()
    monthly = monthly_summary(sales)
    category = category_summary(sales)
    latest = latest_month_comparison(sales)
    print(f"Rows: {len(sales):,}; months: {len(monthly)}; categories: {len(category)}")
    print(f"Recorded revenue: {sales['revenue'].sum():,.2f}")
    print(f"Items sold: {sales['items_sold'].sum():,}")
    print(f"Category order occurrences: {sales['total_orders'].sum():,} (not distinct storewide orders)")
    print("\nLatest monthly totals:")
    print(monthly.tail(3).to_string(index=False))
    print("\nTop categories:")
    print(category.head(5).to_string(index=False))
    print("\nLargest latest-month category revenue changes:")
    print(latest.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
