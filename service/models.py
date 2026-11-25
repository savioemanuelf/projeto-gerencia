from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Produto:
    codigo: int
    preco: Decimal
    estoque: int = 0
