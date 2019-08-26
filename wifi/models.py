
from django.db import models
import django.core.validators

class Classe(models.Model):
    nom = models.CharField(max_length = 15, null = False)

    def __str__(self):
        return self.nom

class Eleve(models.Model):
    nom = models.CharField(max_length = 100, null = False)
    prenom = models.CharField(max_length = 100, null = False)
    classe = models.ForeignKey(Classe, on_delete = models.PROTECT)
    chambre = models.CharField(max_length = 10, null = False)
    annee = models.PositiveSmallIntegerField(choices = [(2017, '2017'), (2018, '2018'),(2019, '2019'),(2020, '2020')], null = False)
    mail = models.EmailField(max_length = 254, blank = True)

    def __str__(self):
        return "{} {} {}".format(self.prenom, self.nom, self.classe)

class Machine(models.Model):
    mac = models.CharField(unique = True, max_length = 17, validators=[django.core.validators.RegexValidator('^[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}$')])
    eleve = models.ForeignKey(Eleve, null = False, on_delete = models.CASCADE)
    type  = models.CharField(max_length = 2, choices = [('P', 'Ordinateur portable'), ('S', 'Smartphone'), ('T', 'Tablette'),])
    actif = models.BooleanField(null = False)

    def __str__(self):
        return self.mac


