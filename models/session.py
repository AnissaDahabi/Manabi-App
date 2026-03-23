class Session:
    def __init__(self, id, cours_id, prof_id, date_session, heure_debut, heure_fin):
        self.id = id
        self.cours_id = cours_id
        self.prof_id = prof_id
        self.date_session = date_session
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin