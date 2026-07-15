from pydantic import BaseModel

# Dichiaro l'oggetto per validare le richieste
class ProdottoIn(BaseModel):
    nome: str
    prezzo: float

class UtenteAuth(BaseModel):
    username: str
    password: str

class PlaylistIn(BaseModel):
    titolo_playlist: str

class VideoIn(BaseModel):
    url_video_youtube: str
    commento: str


class CommentoIn(BaseModel):
    testo: str