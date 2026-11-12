"""Create the static chart shown on the repository's GitHub page."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from sales_analysis import category_summary, load_sales, monthly_summary


def main() -> None:
    sales = load_sales()
    monthly = monthly_summary(sales)
    leaders = category_summary(sales).head(5).sort_values("revenue")
    leaders = leaders.assign(category=leaders["category"].replace(
        {"Fashion Hoodies & Sweatshirts": "Hoodies & Sweatshirts"}
    ))

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), facecolor="#f8fafc")
    fig.subplots_adjust(left=0.07, right=0.98, top=0.79, bottom=0.16, wspace=0.34)
    fig.text(0.06, 0.94, "E-commerce sales at a glance", fontsize=18, weight="bold", color="#102a43")
    fig.text(0.06, 0.86, "Monthly category export  |  Jan 2019–Sep 2026  |  synthetic data", fontsize=10, color="#526579")

    ax = axes[0]
    ax.set_facecolor("#f8fafc")
    ax.plot(monthly["month"], monthly["revenue"], color="#147d80", linewidth=2.3)
    ax.fill_between(monthly["month"], monthly["revenue"], color="#147d80", alpha=0.11)
    ax.set_title("Recorded revenue over time", loc="left", weight="bold", color="#102a43")
    ax.set_ylabel("Revenue (source currency)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:.0f}k"))
    ax.grid(axis="y", alpha=0.2)

    ax = axes[1]
    ax.set_facecolor("#f8fafc")
    ax.barh(leaders["category"], leaders["revenue"], color="#147d80")
    ax.set_title("Top five categories by revenue", loc="left", weight="bold", color="#102a43")
    ax.set_xlabel("Revenue (source currency)")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:.0f}k"))
    ax.grid(axis="x", alpha=0.2)
    ax.set_axisbelow(True)

    output = Path(__file__).parent / "assets" / "sales_preview.png"
    output.parent.mkdir(exist_ok=True)
    fig.savefig(output, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
