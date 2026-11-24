from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# --- 1. DATENBANK SETUP ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./datenbank.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- 2. DATENBANK TABELLE ---
class Eintrag(Base):
    __tablename__ = "eintraege"
    id = Column(Integer, primary_key=True, index=True)
    text_inhalt = Column(String, index=True)


# Erstellt die Datenbankdatei und Tabellen automatisch, falls sie nicht existieren
Base.metadata.create_all(bind=engine)


# Hilfsfunktion, um die Datenbankverbindung für jede Anfrage zu öffnen und zu schließen
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


# --- 3. FASTAPI SETUP & MODELLE ---
app = FastAPI()


class MeinDatenPaket(BaseModel):
    text_eingabe: str


# --- 4. ENDPUNKTE ---
@app.get("/ui")
def lade_weboberflaeche():
    return FileResponse("index.html")


@app.post("/api/daten_senden")
def empfange_daten(paket: MeinDatenPaket, db: DbSession):
    # Neuen Eintrag in die Datenbank schreiben
    neuer_eintrag = Eintrag(text_inhalt=paket.text_eingabe)
    db.add(neuer_eintrag)
    db.commit()
    db.refresh(neuer_eintrag)  # Holt die neue ID aus der Datenbank

    return {"status": "ok", "message": f"Gespeichert unter ID {neuer_eintrag.id}!"}


@app.get("/api/eintraege")
def hole_alle_eintraege(db: DbSession):
    # Alle Einträge aus der Datenbank auslesen
    eintraege = db.query(Eintrag).all()
    return eintraege
