from models import *

ma_liste = MaListe()
ma_liste.set_nombres([1, 3])
ma_liste.save()

# Pour récupérer la liste
liste_recuperee = ma_liste.get_nombres()
