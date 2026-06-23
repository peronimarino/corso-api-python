from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import secrets

#Importo il resto del progetto
from BASE.progetto_prodotti import router as prodotti_router
from BASE.progetto_db import dbinit
from BASE.progetto_utente import router as utenti_router


#Inizializzo il DB
dbinit()

app=FastAPI()

# Configuro il CORS per accettare tutto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Permette l'accesso da qualsiasi sito (Origin)
    allow_credentials=True,
    allow_methods=["*"],          # Permette tutti i metodi (GET, POST, PUT, DELETE, ecc.)
    allow_headers=["*"],          # Permette tutte le intestazioni (Headers)
)

app.include_router(prodotti_router)
app.include_router(utenti_router)

# Creo una chiamata base di benvenuto
@app.get("/")
def home():
    return {"INFO": "Server principale attivo"}
