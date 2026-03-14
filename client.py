import datetime

class Client:
    def __init__(self, client_id: int, name: str, country: str, signup_date: datetime.datetime):
        self.client_id = client_id
        self.name = name
        self.country = country
        self.signup_date = signup_date

    def to_dict(self) -> dict:
        return {
            "client_id": self.client_id,
            "name": self.name,
            "country": self.country,
            "signup_date": self.signup_date.isoformat()
        }

cliente = Client(
    client_id=1234,
    name="Camila",
    country="Colombia",
    signup_date=datetime.datetime.now()
)

print(cliente.to_dict())