from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base

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


# --- 3. FASTAPI SETUP & MODELLE ---
app = FastAPI()


class MeinDatenPaket(BaseModel):
    text_eingabe: str


# --- 4. ENDPUNKTE ---
@app.get("/ui")
def lade_weboberflaeche():
    return FileResponse("index.html")


@app.post("/api/daten_senden")
def empfange_daten(paket: MeinDatenPaket, db: Session = Depends(get_db)):
    # Neuen Eintrag in die Datenbank schreiben
    neuer_eintrag = Eintrag(text_inhalt=paket.text_eingabe)
    db.add(neuer_eintrag)
    db.commit()
    db.refresh(neuer_eintrag)  # Holt die neue ID aus der Datenbank

    return {"status": "ok", "message": f"Gespeichert unter ID {neuer_eintrag.id}!"}


@app.get("/api/eintraege")
def hole_alle_eintraege(db: Session = Depends(get_db)):
    # Alle Einträge aus der Datenbank auslesen
    eintraege = db.query(Eintrag).all()
    return eintraege