# Definiert die Datenstruktur eines Patienten.
# Beispielsweise Patienten-ID, Name, Geburtsdatum und Krankheitsgeschichte (...)


patienten = {}

def patient_hinzufuegen(patient_id, name, alter):
    patienten[patient_id] = {
        "name": name,
        "alter": alter
    }
    return True


def patient_suchen(patient_id):
    return patienten.get(patient_id)


def patient_loeschen(patient_id):
    if patient_id in patienten:
        del patienten[patient_id]
        return True
    return False
