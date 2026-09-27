from dataclasses import dataclass


@dataclass
class Whisky:
    name: str
    price: float | None  # in GBP; None when sold out
    in_stock: bool
    link: str
