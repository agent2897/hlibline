# ХлібЛайн — API

Бекенд інформаційної системи управління виробництвом і збутом хлібокомбінату (навчальний проєкт, група 401).

## Швидкий старт

```bash
git clone https://github.com/agent2897/hlibline.git
cd hlibline
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Документація API: http://127.0.0.1:8000/docs · перевірка: http://127.0.0.1:8000/health

## Тести

```bash
pytest -q
```

## Docker

```bash
docker compose up --build
```

## Структура

```
app/main.py        — API: /health, /products, /orders
tests/test_api.py  — тести (pytest)
.env.example       — змінні середовища (ORDER_CUTOFF_HOUR, MIN_ORDER_SUM)
```

Команда: Миленко (PM), Яцько (BA), Дубчак (backend), Бойко (frontend), Авраменко (mobile), Кіцул (QA).
