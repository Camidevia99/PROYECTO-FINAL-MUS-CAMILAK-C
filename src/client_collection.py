import json
from pathlib import Path
from client import Client


class ClientCollection:

    def __init__(self, clients=None):

        if clients is not None:
            self.clients = clients
        else:
            base_path = Path(__file__).resolve().parent
            file_path = base_path.parent / "data" / "clients.json"

            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.clients = [Client(**client) for client in data]


    def count_clients(self):
        return len(self.clients)


    def get_client_by_id(self, client_id):

        for client in self.clients:
            if client.client_id == client_id:
                return client

        return None


    def clients_by_country(self, country):

        return [client for client in self.clients if client.country == country]