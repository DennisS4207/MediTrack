"""LLM-Anbindung (Claude API) für UI-Design-Ideen und Code-Verbesserungen.

Es werden bewusst nur Quelltext und freie Texte der Entwicklerin bzw. des Entwicklers gesendet,
niemals Patientendaten.
"""
import os

MODELL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")

MODI = {
    "UI-Design-Ideen": (
        "Du berätst bei der Gestaltung von Streamlit-Oberflächen für medizinisches Fachpersonal "
        "(Patientenüberwachung, Vitalwerte, Alarme). Gib 3 bis 5 konkrete, umsetzbare Verbesserungen "
        "zu Übersichtlichkeit, Lesbarkeit, Farbe und Bedienung. Nenne jeweils kurz das Problem und die "
        "Lösung, wenn passend mit einem kleinen Streamlit-Codebeispiel. Antworte auf Deutsch."
    ),
    "Code-Verbesserungen": (
        "Du reviewst Python-Code (Streamlit-Frontend und DDD-Backend). Nenne die wichtigsten Probleme "
        "zu Korrektheit, Lesbarkeit, Fehlerbehandlung, Sicherheit und Tests, nach Wichtigkeit sortiert. "
        "Zeige für jedes Problem eine kurze, konkrete Korrektur. Antworte auf Deutsch."
    ),
}


def konfiguriert() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def frage(modus: str, inhalt: str, wunsch: str = "") -> str:
    """Schickt Code oder UI-Beschreibung an das Modell und liefert die Antwort als Text."""
    if not konfiguriert():
        raise RuntimeError("ANTHROPIC_API_KEY ist nicht gesetzt.")
    import anthropic  # erst hier importieren, damit die App auch ohne das Paket startet

    client = anthropic.Anthropic()
    nachricht = f"{wunsch.strip()}\n\n```\n{inhalt}\n```" if wunsch.strip() else f"```\n{inhalt}\n```"
    antwort = client.messages.create(
        model=MODELL,
        max_tokens=1500,
        system=MODI[modus],
        messages=[{"role": "user", "content": nachricht}],
    )
    return "".join(block.text for block in antwort.content if block.type == "text")
