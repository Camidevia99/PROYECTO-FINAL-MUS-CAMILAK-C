import json
from pathlib import Path

# obtener la carpeta donde está este archivo
base_path = Path(__file__).resolve().parent

# ir a la carpeta data
file_path = base_path.parent / "data" / "clients.json"

# abrir el json
with open(file_path, "r") as file:
    clients = json.load(file)

class Get:

    def get_client_by_id(self, id):
        for client in clients:
            if client["client_id"] == id:
                return client

        return None

# probar la función
g = Get()
client = g.get_client_by_id(2)

print(client)

#
class Country():

    def clients_by_country(self,country):
        result=[]
        for client in clients:
            if client["country"]==country:
                result.append(client)
        return result
    
# probar la función

g = Country()
clientes = g.clients_by_country("Spain")

print(clientes)