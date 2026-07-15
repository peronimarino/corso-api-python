from fastapi import APIRouter, HTTPException
from .progetto_classi_validazione import VideoIn, CommentoIn
import sqlite3

# Creo il mini-gestore delle rotte
router = APIRouter()

def recupera_utente_da_token(token: str):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
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

    return utente["id"]

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

# ==========================
# DETTAGLIO FILM
# ==========================

@router.get("/film/{id_film}")
def dettaglio_film(id_film: int):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM film
        WHERE id = ?
        """,
        (id_film,)
    )

    film = cursor.fetchone()

    conn.close()

    if film is None:
        raise HTTPException(
            status_code=404,
            detail="Film non trovato"
        )

    return film

# ==========================
# AGGIUNGI VIDEO
# ==========================

@router.post("/film/{id_film}/video")
def aggiungi_video(
    id_film: int,
    dati: VideoIn,
    token: str
):

    id_utente = recupera_utente_da_token(token)

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO elementi_video
        (
            film_id,
            utente_id,
            url_video_youtube,
            commento
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            id_film,
            id_utente,
            dati.url_video_youtube,
            dati.commento
        )
    )

    conn.commit()
    conn.close()

    return {
        "messaggio": "Video aggiunto correttamente"
    }

# ==========================
# VIDEO DEL FILM
# ==========================

@router.get("/film/{id_film}/video")
def video_film(id_film: int):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            elementi_video.id,
            elementi_video.url_video_youtube,
            elementi_video.commento,
            utenti.username

        FROM elementi_video

        JOIN utenti
        ON elementi_video.utente_id = utenti.id

        WHERE film_id = ?
        """,
        (id_film,)
    )

    risultato = cursor.fetchall()

    conn.close()

    return risultato

# ==========================
# AGGIUNGI COMMENTO
# ==========================

@router.post("/film/{id_film}/commento")
def aggiungi_commento(
    id_film: int,
    dati: CommentoIn,
    token: str
):

    id_utente = recupera_utente_da_token(token)

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO commenti
        (
            film_id,
            utente_id,
            testo
        )
        VALUES (?, ?, ?)
        """,
        (
            id_film,
            id_utente,
            dati.testo
        )
    )

    conn.commit()
    conn.close()

    return {
        "messaggio": "Commento aggiunto correttamente"
    }

# ==========================
# COMMENTI DEL FILM
# ==========================

@router.get("/film/{id_film}/commenti")
def commenti_film(id_film: int):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            commenti.id,
            commenti.testo,
            utenti.username

        FROM commenti

        JOIN utenti
        ON commenti.utente_id = utenti.id

        WHERE film_id = ?
        """,
        (id_film,)
    )

    risultato = cursor.fetchall()

    conn.close()

    return risultato