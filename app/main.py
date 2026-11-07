"""ХлібЛайн — API прийому замовлень (каркас бекенду для онбордингу команди)."""
import os
from datetime import datetime, time, date, timedelta

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

CUTOFF = time(int(os.getenv('ORDER_CUTOFF_HOUR', '18')))  # прийом замовлень до 18:00
MIN_ORDER_SUM = float(os.getenv('MIN_ORDER_SUM', '500'))

app = FastAPI(title='ХлібЛайн API', version='0.1.0')

PRODUCTS = {
    1: {'name': 'Хліб «Український»', 'price': 32.0},
    2: {'name': 'Батон нарізний', 'price': 28.5},
    3: {'name': 'Багет французький', 'price': 35.0},
}
ORDERS: dict[int, dict] = {}


class Item(BaseModel):
    product_id: int
    qty: int = Field(gt=0)


class OrderIn(BaseModel):
    client: str
    items: list[Item]


def delivery_date(now: datetime) -> date:
    """UC-01: до 18:00 — доставка завтра, після — післязавтра."""
    return now.date() + timedelta(days=1 if now.time() < CUTOFF else 2)


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.get('/products')
def products():
    return [{'id': k, **v} for k, v in PRODUCTS.items()]


@app.post('/orders', status_code=201)
def create_order(order: OrderIn, now: datetime | None = None):
    total = 0.0
    for it in order.items:
        if it.product_id not in PRODUCTS:
            raise HTTPException(404, f'Продукт {it.product_id} не знайдено')
        total += PRODUCTS[it.product_id]['price'] * it.qty
    if total < MIN_ORDER_SUM:
        raise HTTPException(422, f'Мінімальна сума замовлення — {MIN_ORDER_SUM:.0f} грн')
    oid = len(ORDERS) + 1
    ORDERS[oid] = {'id': oid, 'client': order.client, 'items': [i.model_dump() for i in order.items],
                   'total': round(total, 2), 'delivery_date': delivery_date(now or datetime.now()).isoformat(),
                   'status': 'Прийнято'}
    return ORDERS[oid]


@app.get('/orders/{oid}')
def get_order(oid: int):
    if oid not in ORDERS:
        raise HTTPException(404, 'Замовлення не знайдено')
    return ORDERS[oid]
