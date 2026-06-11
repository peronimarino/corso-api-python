import sqlite3
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello from corso-api-python"}

@app.get("/prodotti")
def ottieni_prodotti():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row # Conversione attiva!
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prodotti")
    risultato = cursor.fetchall()
    conn.close()
    return risultato

@app.get("/prodotti/ricerca")
def cerca_prodotto(keyword: str):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM prodotti WHERE nome LIKE ?",
        (f"%{keyword}%",)
    )
    
    risultati = cursor.fetchall()
    conn.close()
    return risultati
