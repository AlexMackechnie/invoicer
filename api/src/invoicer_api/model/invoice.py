from dataclasses import dataclass

@dataclass
class Invoice:
    name: str
    email: str
    address: str
    payment_details: str
    send_to: str
    amount: float
    description: str

