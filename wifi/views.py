from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Eleve

class Login(LoginView):
    template_name = "login.html"


@login_required
def test_vue(request, *args, **kwargs):
    toto = kwargs['toto']
    #import pdb; pdb.set_trace()
    #return render(request, "wifi/bonjour.html", {'toto': toto})
    return HttpResponseRedirect(reverse('bonjour2', args = [toto]))

@method_decorator(login_required, name='dispatch') # applique le décorateur à la méthode dispatch, première appelée.
class test_classe(TemplateView):
    template_name = "wifi/bonjour.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['toto'] = kwargs['toto']+1
        return context

class ListeEleves(ListView):
    model = Eleve

class DetailEleve(DetailView):
    model = Eleve

class UpdateEleve(UpdateView):
    model = Eleve
    fields = ['nom', 'prenom', 'chambre', 'classe', 'annee', 'mail']

    def get_success_url(self):
        return reverse('eleve', args = [self.object.id])
