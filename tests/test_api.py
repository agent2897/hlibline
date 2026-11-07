from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app, delivery_date

client = TestClient(app)


def test_health():
    assert client.get('/health').json() == {'status': 'ok'}


def test_create_order():
    r = client.post('/orders', json={'client': 'АТБ №12', 'items': [{'product_id': 1, 'qty': 20}]})
    assert r.status_code == 201
    assert r.json()['total'] == 640.0


def test_min_sum():
    r = client.post('/orders', json={'client': 'Кіоск', 'items': [{'product_id': 2, 'qty': 1}]})
    assert r.status_code == 422


def test_cutoff():
    assert delivery_date(datetime(2027, 4, 5, 17, 59)).day == 6
    assert delivery_date(datetime(2027, 4, 5, 18, 1)).day == 7
