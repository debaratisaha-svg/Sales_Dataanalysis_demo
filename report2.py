# Sales Data Analysis & Revenue Reporting System with Dashboard

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- FORCE FULL TABLE DISPLAY ----------
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

# ---------- DECORATOR ----------
def log_function(func):
    def wrapper(*args, **kwargs):
        print(f"\n--- {func.__name__} started ---")
        result = func(*args, **kwargs)
        print(f"--- {func.__name__} completed ---")
        return result
    return wrapper


# ---------- LOAD DATA ----------
@log_function
def load_data():
    df = pd.read_csv(r"sales_history.csv")
    df["PurchaseDate"] = pd.to_datetime(df["PurchaseDate"], errors="coerce")
    df.fillna(0, inplace=True)

    print("\n================ FULL SALES DATA TABLE ================\n")
    print(df.to_string(index=False))

    return df


# ---------- CALCULATE REVENUE ----------
@log_function
def calculate_revenue(df):
    df["CalculatedRevenue"] = df["Quantity"] * df["UnitPrice"]

    total = np.sum(df["CalculatedRevenue"])
    average = np.mean(df["CalculatedRevenue"])

    print("\n================ SALES SUMMARY ================")
    print(f"Total Revenue   : ₹{total:.2f}")
    print(f"Average Revenue : ₹{average:.2f}")

    return df


# ---------- TOP PRODUCT & CUSTOMER ----------
@log_function
def top_product_customer(df):
    top_product = df.groupby("Product-category")["CalculatedRevenue"].sum().idxmax()
    top_customer = df.groupby("CustomerID")["CalculatedRevenue"].sum().idxmax()

    print("\n================ TOP PERFORMERS ================")
    print(f"Top Product Category : {top_product}")
    print(f"Top Customer         : {top_customer}")


# ---------- MONTHLY SALES TREND ----------
@log_function
def monthly_sales_trend(df):
    df["Month"] = df["PurchaseDate"].dt.to_period("M")
    monthly = df.groupby("Month")["CalculatedRevenue"].sum().sort_index()

    print("\n================ MONTHLY SALES TREND (TABLE) ================\n")
    print(monthly.to_string())

    return monthly


# ---------- EXPORT ----------
@log_function
def export_report(df):
    df.to_csv("final_sales_report.csv", index=False)
    print("\nFinal sales report exported successfully!")


# ---------- DASHBOARD ----------
@log_function
def sales_dashboard(df):
    df = df.copy()   # avoid warnings
    df["Month"] = df["PurchaseDate"].dt.to_period("M")

    monthly_sales = df.groupby("Month")["CalculatedRevenue"].sum()
    category_sales = df.groupby("Product-category")["CalculatedRevenue"].sum()
    top_customers = (
        df.groupby("CustomerID")["CalculatedRevenue"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    monthly_sales.index = monthly_sales.index.astype(str)

    print("\n================ DASHBOARD GENERATING ================")
    print("Dashboard will open in a graphical window...")
    print("Dashboard image will also be saved as 'sales_dashboard.png'")

    plt.figure(figsize=(14, 10))

    # 1. Monthly Trend
    plt.subplot(2, 2, 1)
    sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xticks(rotation=45)

    # 2. Category Sales
    plt.subplot(2, 2, 2)
    sns.barplot(x=category_sales.index, y=category_sales.values)
    plt.title("Revenue by Product Category")
    plt.xticks(rotation=45)

    # 3. Top Customers
    plt.subplot(2, 2, 3)
    sns.barplot(x=top_customers.index.astype(str), y=top_customers.values)
    plt.title("Top 5 Customers by Revenue")

    # 4. Revenue Distribution
    plt.subplot(2, 2, 4)
    sns.histplot(df["CalculatedRevenue"], bins=10, kde=True)
    plt.title("Revenue Distribution")

    plt.suptitle("Sales Data Analysis Dashboard", fontsize=16)
    plt.tight_layout()

    # SAVE DASHBOARD
    plt.savefig("sales_dashboard.png")

    # SHOW AFTER EVERYTHING IS PRINTED
    plt.show()


# ---------- MAIN ----------
def main():
    df = load_data()
    df = calculate_revenue(df)
    top_product_customer(df)
    monthly_sales_trend(df)
    export_report(df)
    sales_dashboard(df)


# ---------- EXECUTION ----------
if __name__ == "__main__":
    main()