import json
import csv
from pathlib import Path
import pandas as pd

base_path = Path(__file__).resolve().parent
data_path = base_path.parent / "data"


def load_clients():
    with open(data_path / "clients.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_sales():
    sales = []
    with open(data_path / "sales.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sales.append(row)
    return sales


def generate_report():

    clients = load_clients()
    sales = load_sales()

    # -------------------------
    # 1 TOTAL CLIENTES
    # -------------------------
    total_clients = len(clients)

    # -------------------------
    # 2 TOTAL VENTAS (count)
    # -------------------------
    total_sales = len(sales)

    # -------------------------
    # TOTAL INGRESOS
    # -------------------------
    total_revenue = sum(float(s["amount"]) for s in sales)

    # -------------------------
    # 3 TOTAL POR CLIENTE
    # -------------------------
    sales_by_client = {}
    count_sales_by_client = {}

    for sale in sales:

        cid = int(sale["client_id"])
        amount = float(sale["amount"])

        sales_by_client.setdefault(cid, 0)
        sales_by_client[cid] += amount

        count_sales_by_client.setdefault(cid, 0)
        count_sales_by_client[cid] += 1

    # -------------------------
    # 5 PROMEDIO POR CLIENTE
    # -------------------------
    avg_sales_by_client = {}

    for cid in sales_by_client:
        avg_sales_by_client[cid] = round(
            sales_by_client[cid] / count_sales_by_client[cid], 2
        )

    # -------------------------
    # 6 CLIENTE CON MAYOR GASTO
    # -------------------------
    max_client = max(sales_by_client, key=sales_by_client.get)

    # -------------------------
    # 7 VENTAS POR CATEGORIA
    # -------------------------
    df = pd.read_csv(data_path / "sales.csv")

    sales_by_category = (
        df.groupby("category")["amount"].sum().to_dict()
    )

    # -------------------------
    # 8 CLIENTE CON MÁS ELECTRONICS
    # -------------------------
    electronics = df[df["category"] == "Electronics"]

    top_client = (
        electronics.groupby("client_id")["amount"].sum().idxmax()
    )

    # -------------------------
    # 9 CLIENTES CON GASTO MINIMO
    # -------------------------
    min_amount = 500
    clients_with_min_spending = 0

    for client in clients:

        cid = int(client["client_id"])

        if sales_by_client.get(cid, 0) > min_amount:
            clients_with_min_spending += 1

    # -------------------------
    # 10 VENTAS POR MES
    # -------------------------
    df["date"] = pd.to_datetime(df["date"])
    df["year_month"] = df["date"].dt.to_period("M")

    monthly_sales = (
        df.groupby("year_month")["amount"]
        .sum()
        .astype(float)
        .to_dict()
    )

    # -------------------------
    # CLIENTES CON MÉTRICAS
    # -------------------------
    clients_with_totals = []

    for client in clients:

        cid = int(client["client_id"])

        total_spent = sales_by_client.get(cid, 0)
        sale_count = count_sales_by_client.get(cid, 0)

        average_sale = (
            round(total_spent / sale_count, 2) if sale_count > 0 else 0
        )

        new_client = {
            "client_id": cid,
            "name": client["name"],
            "country": client["country"],
            "signup_date": client["signup_date"],
            "total_spent": total_spent,
            "sale_count": sale_count,
            "average_sale": average_sale
        }

        clients_with_totals.append(new_client)

    # -------------------------
    # CLIENTE TOP POR PAÍS
    # -------------------------
    top_client_by_country = {}

    for client in clients_with_totals:

        country = client["country"]
        total_spent = client["total_spent"]

        if country not in top_client_by_country:
            top_client_by_country[country] = client

        else:
            if total_spent > top_client_by_country[country]["total_spent"]:
                top_client_by_country[country] = client

    top_client_by_country = {
        country: data["client_id"]
        for country, data in top_client_by_country.items()
    }

    # -------------------------
    # REPORTE FINAL
    # -------------------------
    return {
        "summary": {
            "total_clients": total_clients,
            "total_sales": total_sales,
            "total_revenue": total_revenue,
            "max_client": max_client,
            "clients_with_min_spending": clients_with_min_spending
        },
        "clients": clients_with_totals,
        "sales_by_client": sales_by_client,
        "count_sales_by_client": count_sales_by_client,
        "avg_sales_by_client": avg_sales_by_client,
        "sales_by_category": sales_by_category,
        "top_client_electronics": int(top_client),
        "monthly_sales": monthly_sales,
        "top_client_by_country": top_client_by_country
    }