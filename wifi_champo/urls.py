"""wifi_champo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wifi.views import test_vue, test_classe, ListeEleves, UpdateEleve, DetailEleve, Login, UpdateMachine, CreateEleve, CreateMachine

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bonjour/<int:toto>', test_vue, name='bonjour'),
    path('bonjour2/<int:toto>', test_classe.as_view(), name = "bonjour2"),
    path('eleves/', ListeEleves.as_view(), name="eleves"),
    path('eleve/<int:pk>/update', UpdateEleve.as_view(), name="update_eleve"),
    path('eleve/<int:pk>', DetailEleve.as_view(), name="eleve"),
    path('login/', Login.as_view(), name="login"),
    path('machine/<int:pk>/update', UpdateMachine.as_view(), name="update_machine"),
    path('new_eleve/', CreateEleve.as_view(), name="create_eleve"),
    path('new_machine/<int:eleve>', CreateMachine.as_view(), name="create_machine"),
]
