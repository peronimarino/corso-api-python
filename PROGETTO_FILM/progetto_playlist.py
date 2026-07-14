from fastapi import APIRouter, HTTPException
from .progetto_classi_validazione import PlaylistIn
import sqlite3

router = APIRouter()


# ==========================
# FUNZIONE DI SUPPORTO
# ==========================

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


# ==========================
# CREA PLAYLIST
# ==========================

@router.post("/playlist")
def crea_playlist(
    dati: PlaylistIn,
    token: str
):

    id_utente = recupera_utente_da_token(token)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO playlist
        (titolo_playlist, utente_id)
        VALUES (?, ?)
        """,
        (
            dati.titolo_playlist,
            id_utente
        )
    )

    conn.commit()
    conn.close()

    return {
        "messaggio": "Playlist creata correttamente"
    }


# ==========================
# ELENCO PLAYLIST DELL'UTENTE
# ==========================

@router.get("/playlist")
def mie_playlist(token: str):

    id_utente = recupera_utente_da_token(token)

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, titolo_playlist
        FROM playlist
        WHERE utente_id = ?
        """,
        (id_utente,)
    )

    risultato = cursor.fetchall()

    conn.close()

    return risultato

# ==========================
# VISUALIZZAZIONE PANORAMICA PUBBLICA DELLE PLAYLIST
# ==========================
@router.get("/playlist/pubbliche")
def playlist_pubbliche():

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            playlist.id,
            playlist.titolo_playlist,
            utenti.username
        FROM playlist
        JOIN utenti
        ON playlist.utente_id = utenti.id
    """)

    risultato = cursor.fetchall()

    conn.close()

    return risultato

# ==========================
# DETTAGLIO PLAYLIST PUBBLICA
# ==========================

@router.get("/playlist/pubblica/dettaglio")
def dettaglio_playlist_pubblica(
    playlist_id: int
):

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            film.id,
            film.titolo,
            film.anno
        FROM playlist_film

        JOIN film
        ON playlist_film.film_id = film.id

        WHERE playlist_film.playlist_id = ?
        """,
        (playlist_id,)
    )

    risultato = cursor.fetchall()

    conn.close()

    return risultato

# ==========================
# AGGIUNGI FILM A PLAYLIST
# ==========================

@router.post("/playlist/aggiungi-film")
def aggiungi_film_playlist(
    playlist_id: int,
    film_id: int,
    token: str
):

    id_utente = recupera_utente_da_token(token)

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM playlist
        WHERE id = ?
        AND utente_id = ?
        """,
        (
            playlist_id,
            id_utente
        )
    )

    playlist = cursor.fetchone()

    if playlist is None:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Playlist non trovata"
        )

    cursor.execute(
        """
        SELECT id
        FROM film
        WHERE id = ?
        """,
        (film_id,)
    )

    film = cursor.fetchone()

    if film is None:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Film non trovato"
        )

    try:

        cursor.execute(
            """
            INSERT INTO playlist_film
            (playlist_id, film_id)
            VALUES (?, ?)
            """,
            (
                playlist_id,
                film_id
            )
        )

        conn.commit()

    except sqlite3.IntegrityError:

        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Film già presente nella playlist"
        )

    conn.close()

    return {
        "messaggio": "Film aggiunto alla playlist"
    }


# ==========================
# DETTAGLIO PLAYLIST
# ==========================

@router.get("/playlist/dettaglio")
def dettaglio_playlist(
    playlist_id: int,
    token: str
):

    id_utente = recupera_utente_da_token(token)

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM playlist
        WHERE id = ?
        AND utente_id = ?
        """,
        (
            playlist_id,
            id_utente
        )
    )

    playlist = cursor.fetchone()

    if playlist is None:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Playlist non trovata"
        )

    cursor.execute(
        """
        SELECT
            film.id,
            film.titolo,
            film.anno
        FROM playlist_film

        JOIN film
        ON playlist_film.film_id = film.id

        WHERE playlist_film.playlist_id = ?
        """,
        (playlist_id,)
    )

    risultato = cursor.fetchall()

    conn.close()

    return risultato

# ==========================
# ELIMINA PLAYLIST
# ==========================

@router.delete("/playlist")
def elimina_playlist(
    playlist_id: int,
    token: str
):

    id_utente = recupera_utente_da_token(token)

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM playlist
        WHERE id = ?
        AND utente_id = ?
        """,
        (
            playlist_id,
            id_utente
        )
    )

    if cursor.rowcount == 0:

        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Playlist non trovata"
        )

    conn.commit()
    conn.close()

    return {
        "messaggio": "Playlist eliminata correttamente"
    }

