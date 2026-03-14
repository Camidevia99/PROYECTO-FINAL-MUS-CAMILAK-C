import csv
from pathlib import Path

# obtener la carpeta donde está este archivo
base_path = Path(__file__).resolve().parent

# ir a la carpeta data
file_path = base_path.parent / "data" / "sales.csv"
sales=[]
# abrir el json
with open(file_path, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        sales.append(row)

#Todas las ventas de un cliente.

class Sales:
    def sales_by_client(self,client_id):
        result=[]
        for client in sales:
            if client["client_id"] == str(client_id):
                result.append(client)
        return result

#Total de ventas de un cliente

class Amount(Sales):
  def total_amount_by_client(self, client_id):
        # Usamos la función heredada sales_by_client
        client_sales = self.sales_by_client(client_id)
        
        # Sumamos los montos
        total = sum(float(sale["amount"]) for sale in client_sales)
        return total

#Suma de ventas por categoria

class Category:
    def total_amount_by_category(self, category_name):
        # Filtramos ventas por categoría
        category_sales = [sale for sale in sales if sale["category"] == str(category_name)]
        
        # Sumamos los montos de esa categoría
        total = sum(float(sale["amount"]) for sale in category_sales)
        
        return total


#Media de gasto de venta para un cliente
import statistics

class Average(Sales):
    def average_sale_by_client(self, client_id):
        # Obtenemos las ventas del cliente usando la función heredada
        client_sales = self.sales_by_client(client_id)
        
        # Extraemos solo los montos como float
        amounts = [float(sale["amount"]) for sale in client_sales]
        
        # Evitamos error si no tiene ventas
        if len(amounts) == 0:
            return 0
        
        # Calculamos la media usando statistics.mean
        media = statistics.mean(amounts)
        return media