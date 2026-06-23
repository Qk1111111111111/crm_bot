from fastapi import FastAPI
import psycopg
import keys as const

DB_URL = f"postgresql://{const.LOG}:{const.PASS}@{const.DB_HOST}:{const.DB_PORT}/{const.DB_DATABASE}"

app = FastAPI()

@app.get("/clients")
def clients():
    with psycopg.connect(
        DB_URL
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM clients
            """)
            return cur.fetchall()
print("API STARTED", flush=True)