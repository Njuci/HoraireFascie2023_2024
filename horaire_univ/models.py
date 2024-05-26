from django.db import models
import json

class MaListe(models.Model):
    nombres = models.TextField()

    def set_nombres(self, liste):
        self.nombres = json.dumps(liste)

    def get_nombres(self):
        return json.loads(self.nombres)
