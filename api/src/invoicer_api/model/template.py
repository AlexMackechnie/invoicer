from dataclasses import dataclass
from invoicer_api.model.invoice import Invoice

@dataclass
class Template:
    template_name: str
    invoice: Invoice

