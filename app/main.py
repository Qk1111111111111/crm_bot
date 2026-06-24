from fastapi import FastAPI
import psycopg
import keys as const
from fastapi.encoders import jsonable_encoder

DB_URL = f"postgresql://{const.LOG}:{const.PASS}@{const.DB_HOST}:{const.DB_PORT}/{const.DB_DATABASE}"

app = FastAPI()

@app.get("/clients")
def clients():
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM clients")
            rows = cur.fetchall()

    return [
        {
            "id": r[0],
            "telegram": r[1],
            "full_name": r[2],
            "full_name2": r[3],
            "birthday": str(r[4]),
            "phone": r[5],
            "tg": r[6],
            "payment_date": str(r[7]) if r[7] else None,
            "status": r[8],
            "created_at": str(r[9]),
        }
        for r in rows
    ]

@app.get("/payments")
def payments():
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM payments")
            rows = cur.fetchall()

    return [
        {
            "id": r[0],
            "client_id": r[1],
            "product_id": r[2],
            "created_at": str(r[3]),
            "payment_method": r[4],
            "comment": r[5],
            "payment_date": str(r[6]) if r[6] else None,
        }
        for r in rows
    ]

@app.get("/visits")
def visits():
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM visits")
            rows = cur.fetchall()

    return [
        {
            "id": r[0],
            "client_id": r[1],
            "scheduled_date": str(r[2]) if r[2] else None,
            "attended": r[3],
            "created_at": str(r[4]),
            "comment": r[5],
        }
        for r in rows
    ]

@app.get("/products")
def products():
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()

    return [
        {
            "id": r[0],
            "product_id": r[1],
            "name": r[2],
            "description": r[3],
            "price": float(r[4]) if r[4] is not None else None,
            "number": r[5],
            "time_frame": r[6],
            "start_dt": str(r[7]) if r[7] else None,
            "end_dt": str(r[8]) if r[8] else None,
            "type": r[9],
            "status": r[10]
        }
        for r in rows
    ]
    
print("API STARTED", flush=True)