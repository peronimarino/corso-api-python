from fastapi import APIRouter, HTTPException
from .progetto_classi_validazione import ProdottoIn
import sqlite3

# Creo il mini-gestore delle rotte
router = APIRouter()