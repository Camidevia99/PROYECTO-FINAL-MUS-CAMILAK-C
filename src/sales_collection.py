import csv
from pathlib import Path
from sale import Sale


class SalesCollection:

    def __init__(self, sales=None):

        base_path = Path(__file__).resolve().parent
        file_path = base_path.parent / "data" / "sales.csv"

        self.sales = []

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                sale = Sale(
                    sale_id=row["sale_id"],
                    client_id=int(row["client_id"]),
                    product=row["product"],
                    category=row["category"],
                    amount=float(row["amount"]),
                    date=row["date"],
                )

                self.sales.append(sale)


    def sales_by_client(self, client_id):

        return [sale for sale in self.sales if sale.client_id == client_id]


    def total_sales(self):

        return sum(sale.amount for sale in self.sales)