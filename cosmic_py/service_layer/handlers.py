from typing import Optional
from datetime import date
import email

from domain import models, events
from .unit_of_work import AbstractUnitOfWork


class InvalidSku(Exception):
    pass


def add_batch(event: events.BatchCreated, uow: AbstractUnitOfWork):
    with uow:
        product = uow.products.get(sku=event.sku)
        if product is None:
            product = models.Product(event.sku, batches=[])
            uow.products.add(product)
        product.batches.append(models.Batch(event.ref, event.sku, event.qty, event.eta))
        uow.commit()


def allocate(event: events.AllocationRequired, uow: AbstractUnitOfWork) -> str:
    line = models.OrderLine(event.orderid, event.sku, event.qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = product.allocate(line)
        uow.commit()
    return batchref


def send_out_of_stock_notification(event: events.OutOfStock, uow: AbstractUnitOfWork):
    email.send(
        "stock@made.com", f"Out of stock for {event.sku}",
    )