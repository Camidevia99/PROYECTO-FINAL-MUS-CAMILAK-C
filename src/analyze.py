
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

    # 1. Contar clientes
    total_clients = len(clients)

    # 2. Total ventas
    total_sales = sum(float(s["amount"]) for s in sales)

    # 3. Total ventas por cliente
    sales_by_client = {}
    for s in sales:
        cid = int(s["client_id"])
        sales_by_client.setdefault(cid, 0)
        sales_by_client[cid] += float(s["amount"])

    # 4. Número de ventas por cliente
    count_sales_by_client = {}
    for s in sales:
        cid = int(s["client_id"])
        count_sales_by_client.setdefault(cid, 0)
        count_sales_by_client[cid] += 1

    # 5. Promedio de ventas por cliente
    avg_sales_by_client = {}
    for cid in sales_by_client:
        avg_sales_by_client[cid] = sales_by_client[cid] / count_sales_by_client[cid]

    # 6. Cliente con mayor gasto
    max_client = max(sales_by_client, key=sales_by_client.get)

    # 7. Ventas por categoría
    df = pd.read_csv(data_path / "sales.csv")
    sales_by_category = df.groupby("category")["amount"].sum().to_dict()

    # 8. Cliente con más ventas en Electronics
    electronics = df[df["category"] == "Electronics"]
    top_client = electronics.groupby("client_id")["amount"].sum().idxmax()

    return {
        "total_clients": total_clients,
        "total_sales": total_sales,
        "sales_by_client": sales_by_client,
        "count_sales_by_client": count_sales_by_client,
        "avg_sales_by_client": avg_sales_by_client,
        "max_client": max_client,
        "sales_by_category": sales_by_category,
        "top_client_electronics": int(top_client),
    }



