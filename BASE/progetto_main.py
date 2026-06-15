from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#Importo il resto del progetto
from BASE.progetto_prodotti import router as prodotti_router
from BASE.progetto_db import dbinit

#Inizializzo il DB
dbinit()

app=FastAPI()

app.include_router(prodotti_router)

# Creo una chiamata base di benvenuto
@app.get("/")
def home():
    return {"INFO": "Server principale attivo"}
