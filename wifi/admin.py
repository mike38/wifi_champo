from django.contrib import admin

from .models import Eleve, Classe, Machine

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ["nom",]

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ["nom", "prenom", "classe", "chambre", "annee", "mail"]

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ["mac", "type", "actif", "eleve"]
