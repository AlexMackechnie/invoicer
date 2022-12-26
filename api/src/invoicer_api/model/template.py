from dataclasses import dataclass

@dataclass
class Template:
    template_name: str
    name: str
    address: str
    payment_details: str
    send_to: str
    amount: float
    description: str

