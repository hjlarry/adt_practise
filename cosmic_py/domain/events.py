from typing import Optional
from dataclasses import dataclass
from datetime import date


class Event:
    pass


@dataclass
class OutOfStock(Event):
    sku: str


@dataclass
class BatchCreated(Event):
    ref: str
    sku: str
    qty: str
    eta: Optional[date] = None


@dataclass
class AllocationRequired(Event):
    orderid: str
    sku: str
    qty: int