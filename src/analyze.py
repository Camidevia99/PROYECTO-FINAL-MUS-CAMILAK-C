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

    # ---------------------------
    # 1. TOTAL CLIENTES
    # ---------------------------
    total_clients = len(clients)

    # ---------------------------
    # 2. TOTAL VENTAS
    # ---------------------------
    total_sales = len(sales)
    # TOTAL INGRESOS (dinero total)
    total_revenue = sum(float(s["amount"]) for s in sales)  
    # ---------------------------
    # 3. VENTAS POR CLIENTE
    # ---------------------------
    sales_by_client = {}

    for s in sales:
        cid = int(s["client_id"])
        sales_by_client.setdefault(cid, 0)
        sales_by_client[cid] += float(s["amount"])

    # ---------------------------
    # 4. NUMERO DE VENTAS POR CLIENTE
    # ---------------------------
    count_sales_by_client = {}

    for s in sales:
        cid = int(s["client_id"])
        count_sales_by_client.setdefault(cid, 0)
        count_sales_by_client[cid] += 1

    # ---------------------------
    # 5. PROMEDIO POR CLIENTE
    # ---------------------------
    avg_sales_by_client = {}

    for cid in sales_by_client:
        avg_sales_by_client[cid] = (
            sales_by_client[cid] / count_sales_by_client[cid]
        )

    # ---------------------------
    # 6. CLIENTE CON MAYOR GASTO
    # ---------------------------
    max_client = max(sales_by_client, key=sales_by_client.get)

    # ---------------------------
    # 7. VENTAS POR CATEGORIA
    # ---------------------------
    df = pd.read_csv(data_path / "sales.csv")

    sales_by_category = df.groupby("category")["amount"].sum().to_dict()

    # ---------------------------
    # 8. CLIENTE CON MAS ELECTRONICS
    # ---------------------------
    electronics = df[df["category"] == "Electronics"]

    top_client = electronics.groupby("client_id")["amount"].sum().idxmax()

    # ---------------------------
    # 9. CLIENTES CON GASTO MINIMO
    # ---------------------------
    def total_amount_by_client(client_id):
        total = 0
        for sale in sales:
            if int(sale["client_id"]) == client_id:
                total += float(sale["amount"])
        return total

    min_amount = 500
    clients_with_min_spending = 0

    for client in clients:
        total = total_amount_by_client(client["client_id"])
        if total > min_amount:
            clients_with_min_spending += 1

    # ---------------------------
    # 10. VENTAS MES A MES
    # ---------------------------
    df["date"] = pd.to_datetime(df["date"])

    df["year_month"] = df["date"].dt.to_period("M")

    monthly_sales = (
        df.groupby("year_month")["amount"]
        .sum()
        .astype(float)
        .to_dict()
    )

    # ---------------------------
    # REPORTE FINAL
    # ---------------------------
    clients_with_totals = []

    for client in clients:

        cid = int(client["client_id"])

    total_spent = sales_by_client.get(cid, 0)

    new_client = {
        "client_id": cid,
        "name": client["name"],
        "country": client["country"],
        "signup_date": client["signup_date"],
        "total_spent": total_spent
    }

    clients_with_totals.append(new_client)
    
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
    "monthly_sales": monthly_sales
}


