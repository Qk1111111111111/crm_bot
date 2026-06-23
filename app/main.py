from fastapi import FastAPI
import psycopg
import keys as const
from fastapi.responses import JSONResponse

DB_URL = f"postgresql://{const.LOG}:{const.PASS}@{const.DB_HOST}:{const.DB_PORT}/{const.DB_DATABASE}"

app = FastAPI()

@app.get("/clients")
def clients():
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM clients")
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]

    result = [
        dict(zip(columns, row))
        for row in rows
    ]

    return JSONResponse(content=result)

print("API STARTED", flush=True)