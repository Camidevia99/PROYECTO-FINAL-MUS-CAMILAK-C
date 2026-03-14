import csv
from pathlib import Path
from sale import Sale


class SalesCollection:

    def __init__(self, sales=None):

        if sales is not None:
            self.sales = sales
            return

        base_path = Path(__file__).resolve().parent
        file_path = base_path.parent / "data" / "sales.csv"

        self.sales = []

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                sale = Sale(
                    row["sale_id"],
                    int(row["client_id"]),
                    row["product"],
                    row["category"],
                    float(row["amount"]),
                    row["date"]
                )

                self.sales.append(sale)

    def sales_by_client(self, client_id):

        return [sale for sale in self.sales if sale.client_id == client_id]
    
    def total_amount_by_client(self, client_id):

        total = 0

        for sale in self.sales:
         if sale.client_id == client_id:
            total += sale.amount

         return total

    def total_sales(self):

        return len(self.sales)