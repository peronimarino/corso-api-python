from .progetto_classi_validazione import UtenteAuth
from fastapi import APIRouter, HTTPException
import sqlite3
import hashlib
import secrets

router = APIRouter()

# =========================
# HASH PASSWORD
# =========================

def calcola_hash(password_chiaro: str) -> str:
    return hashlib.sha256(
        password_chiaro.encode("utf-8")
    ).hexdigest()


# =========================
# REGISTER
# =========================

@router.post("/register")
def registra_utente(dati: UtenteAuth):

    password_sicura = calcola_hash(dati.password)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO utenti
            (username, password_hash)
            VALUES (?, ?)
            """,
            (
                dati.username,
                password_sicura
            )
        )

        conn.commit()

    except sqlite3.IntegrityError:

        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Username già esistente"
        )

    conn.close()

    return {
        "messaggio": "Utente registrato correttamente"
    }


# =========================
# LOGIN
# =========================

@router.post("/login")
def login_utente(dati: UtenteAuth):

    hash_da_verificare = calcola_hash(
        dati.password
    )

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, password_hash
        FROM utenti
        WHERE username = ?
        """,
        (dati.username,)
    )

    utente = cursor.fetchone()

    if utente is None:

        conn.close()

        raise HTTPException(
            status_code=401,
            detail="Credenziali errate"
        )

    if utente["password_hash"] != hash_da_verificare:

        conn.close()

        raise HTTPException(
            status_code=401,
            detail="Credenziali errate"
        )

    token_sessione = secrets.token_hex(16)

    cursor.execute(
        """
        UPDATE utenti
        SET token = ?
        WHERE id = ?
        """,
        (
            token_sessione,
            utente["id"]
        )
    )

    conn.commit()

    conn.close()

    return {
        "token": token_sessione
    }


# =========================
# PROFILO PROTETTO
# =========================

@router.get("/profilo")
def mostra_profilo_utente(token: str):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username
        FROM utenti
        WHERE token = ?
        """,
        (token,)
    )

    utente = cursor.fetchone()

    conn.close()

    if utente is None:

        raise HTTPException(
            status_code=401,
            detail="Token non valido"
        )

    return {
        "id": utente["id"],
        "username": utente["username"]
    }

@router.post("/logout")
def logout_utente(token: str):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE utenti
        SET token = NULL
        WHERE token = ?
        """,
        (token,)
    )

    conn.commit()
    conn.close()

    return {
        "messaggio": "Logout effettuato correttamente"
    }