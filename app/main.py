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
    
print("API STARTED", flush=True)