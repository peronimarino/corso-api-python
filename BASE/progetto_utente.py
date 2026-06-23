from .progetto_classi_validazione import UtenteAuth
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import hashlib
import secrets

#creo il mini-gestore delle rotte
router = APIRouter()


def calcola_hash(password_chiaro: str)->str:
    # Calcola l'hash SHA-256 della password in chiaro
    hash_risultato = hashlib.sha256(password_chiaro.encode('utf-8')).hexdigest()
    return hash_risultato

@router.post("/register")
def register(utente: UtenteAuth):
    # Calcolo l'hash della password
    password_hash = calcola_hash(utente.password)

    # Inserisco l'utente nel database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO utenti (username, password_hash) VALUES (?, ?)",
                       (utente.username, password_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username già esistente")
    
    conn.close()
    return {"status": "Utente registrato con successo"}

@router.post("/login")
def login(dati: UtenteAuth):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 1. Recupero utente tramite username
    cursor.execute(
        "SELECT id, password_hash FROM utenti WHERE username = ?",
        (dati.username,)
    )
    utente = cursor.fetchone()

    # 2. Calcolo hash della password inviata
    hash_inserito = calcola_hash(dati.password)

    # 3. Controllo credenziali
    if utente is None or utente[1] != hash_inserito:
        raise HTTPException(
            status_code=401,
            detail="Credenziali errate"
        )

    # 4. Generazione token sessione
    token_sessione = secrets.token_hex(16)

    # 5. Salvataggio token nel DB
    cursor.execute(
        "UPDATE utenti SET token = ? WHERE id = ?",
        (token_sessione, utente[0])
    )
    conn.commit()
    conn.close()

    # 6. Risposta al client
    return {"token":"Login effetuato con successo", "value": token_sessione}

@router.get("/profilo")
def profilo(token: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # 1. Cerchiamo l'utente proprietario del token
    cursor.execute("SELECT username FROM utenti WHERE token = ?", (token,))
    utente = cursor.fetchone()

    # 2. Controllo sicurezza
    if utente is None:
        conn.close()
        raise HTTPException(status_code=401, detail="Pass non valido!")

    username_utente_reale = utente[0]
    conn.close()

    # 3. Risposta di successo
    return {
        "status": "Accesso consentito",
        "username": username_utente_reale
    }
