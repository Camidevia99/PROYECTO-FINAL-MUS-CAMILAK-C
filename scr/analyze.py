
import json
import csv
from pathlib import Path

# obtener la carpeta donde está este archivo
base_path = Path(__file__).resolve().parent

# =========================
# 1. CONTAR CLIENTES
# =========================

file_path = base_path.parent / "data" / "clients.json"

with open(file_path, "r", encoding="utf-8") as file:
    clients = json.load(file)

class Get:
      
    def count_clients(self):
        return len(clients)

# crear objeto
g = Get()

# calcular número de clientes
total_clients = g.count_clients()
print("=========================")
print(" 1. CONTAR CLIENTES")
print(" =========================")
print(f"Hay {total_clients} clientes en el JSON")


# =========================
# 2. TOTAL DE VENTAS
# =========================

file_path = base_path.parent / "data" / "sales.csv"

sales = []

with open(file_path, "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        sales.append(row)

class Sales:

    def total_sales(self):
        total = sum(float(sale["amount"]) for sale in sales)
        return total

s = Sales()

total_sales = s.total_sales()
print("=========================")
print(" 2. TOTAL VENTAS ")
print(" =========================")
print(f"El total de ventas es {total_sales} Euros")

# =========================
# 3. TOTAL VENTAS POR CLIENTE
# =========================
from sales_collection import Sales, Amount

# crear objetos
s = Sales()
g = Amount()

# obtener datos
clientes = g.total_amount_by_client(1)
sales_client = s.sales_by_client(1)

print("=========================")
print(" 3.TOTAL VENTAS Y DESGLOSE DE VENTAS POR CLIENTE ")
print(" =========================")
print(f"Total vendido por el cliente: {clientes} Euros")
print("Ventas del cliente:")
print(sales_client)

# =========================
# 4. VENTAS POR CLIENTE
# =========================

# Simplemente la longitud de sales_by_client(id)
sales_client = s.sales_by_client(1)
longitud= len(sales_client)
print("=========================")
print(" 4.VENTAS POR CLIENTE ")
print(" =========================")
print(longitud)

# =========================
# 5. INGRESO PROMEDIO DE VENTA POR CADA CLIENTE 
# =========================

from sales_collection import Average

a=Average()

promedio=a.average_sale_by_client(1)
print("=========================")
print(" 5.PROMEDIO DE VENTA POR CLIENTE ")
print(" =========================")
print(promedio)

# =========================
# 6. CLIENTE CON MAYOR GASTO POR PAIS 
# =========================
# Cruce de datos:
# Agrupar clientes por country (POO)
# Calcular gastos por cliente (colección de ventas)
# Elegir el de mayor total.

from client_collection import Country
from collections import defaultdict

print("=========================")
print(" 6.CLIENTE CON MAYOR GASTO POR PAIS ")
print(" =========================")

# Agrupar clientes por country (POO)

c=Country()

clients_spain = c.clients_by_country("Spain")

print(f"los clientes de Spain son {clients_spain}")

# Calcular gastos por cliente (colección de ventas)

clientes_1 = g.total_amount_by_client(1)
clientes_2 = g.total_amount_by_client(2)
clientes_3 = g.total_amount_by_client(3)
print(f"Las ventas del cliente Spain es {clientes_1}")
print(f"Las ventas del cliente Germany es {clientes_2}")
print(f"Las ventas del cliente France es {clientes_3}")

#Elegir el mayor total

mayor= [clientes_1,clientes_2,clientes_3]
print(f"El mayor valor es pertenece a Germany con un total de {max(mayor)} €")

# =========================
# 7. TOTAL DE VENTAS POR CATEGORIA
# =========================

# Usando pandas:
# Agrupar por categoría → sum amounts
# (df.groupby(“category”) [“amount”].sum())

import pandas as pd

df = pd.read_csv("data/sales.csv")

total_por_categoria = df.groupby("category")["amount"].sum()

print("=========================")
print(" 7.TOTAL DE VENTAS POR CATEGORIA ")
print(" =========================")
print(total_por_categoria)

# =========================
# 8. CLIENTE CON MAS VENTAS EN UNA CATEGORIA ESPECIFICA
# =========================
# Combina:
# filtro por categoría (función pura)
# filtrado por cliente.
# contar ventas.
# devolver el cliente con máximo.

print("=========================")
print(" 8. CLIENTE CON MAS VENTAS EN UNA CATEGORIA ESPECIFICA")
print("=========================")

# Filtrar por categoria
filtered = df[df["category"] == "Electronics"]

# Sumar el valor de ventas por cliente
sales_by_client = filtered.groupby("client_id")["amount"].sum()

# Cliente con mayor venta
top_client = sales_by_client.idxmax()
max_sales = sales_by_client.max()

print(f"El cliente con más ventas es {top_client}")
print(f"El valor total de sus ventas es {max_sales} €")




