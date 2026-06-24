from fastapi import APIRouter, HTTPException
from .progetto_classi_validazione import ProdottoIn
import sqlite3

# Creo il mini-gestore delle rotte
router = APIRouter()

@router.get("/film")
def lista_film():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM film")
    risultato = cursor.fetchall()
    conn.close()
    return risultato

@router.get("/film/ricerca")
def cerca_film(keyword: str):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM film WHERE titolo LIKE ?",
        (f"%{keyword}%",)
    )
    
    risultati = cursor.fetchall()
    conn.close()
    if not risultati:
        raise HTTPException(status_code=404, detail="Film non trovato")
    return risultati