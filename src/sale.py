import datetime

class Sale:
    def __init__(self, sale_id: int, client_id: int, product: str, category:str, amount:float, date:datetime):
        self.sale_id = sale_id
        self.client_id = client_id
        self.product = product
        self.category = category
        self.amount= amount
        self.date= date

    def to_dict(self) -> dict:
        return {
            "sale_id": self.sale_id,
            "client_id": self.client_id,
            "product": self.product,
            "category": self.category,
            "amount": self.amount,
            "date": self.date.isoformat()
        }
sale = Sale(
    sale_id=1234,
    client_id=1040,
    product="vaso",
    category="electronica",
    amount= 1213,
    date=datetime.datetime.now()
)

print(sale.to_dict())