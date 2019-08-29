import csv, io
import pexpect, sys, re
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Eleve, Machine, Classe

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

def data_upload(request):
    template = "wifi/data_upload.html"
    if request.method == "GET" :
        return render (request,template)
    csv_file=request.FILES['file']
    if not csv_file.name.endswith('.csv') :
        messages.error(request, 'this is not a CSV file')
        return render (request,template)
    data_set = csv_file.read().decode('UTF-8')
    io_string= csv.reader(io.StringIO(data_set),delimiter=";",quotechar=None)
    head=next(io_string)
    print(head)
    for column in io_string:
        print(column)
        classeid, created = Classe.objects.get_or_create(
            nom = column[head.index('classe') ]
        )
        eleveid , created = Eleve.objects.get_or_create(
            nom = column[head.index('nom') ],
            prenom =  column[head.index('prenom') ],
            classe = classeid,
            chambre = column[head.index('chambre') ],
            annee = column[head.index('annee') ],
            mail = column[head.index('mail') ]
        )
        _ , created = Machine.objects.update_or_create(
            mac = column[head.index('mac')],
            eleve = eleveid,
            type = column[head.index('type')],
            actif = column[head.index('actif')]
        )
    context={}
    return render(request, template, context)

class ListeEleves(ListView):
    model = Eleve

class DetailEleve(DetailView):
    model = Eleve

class UpdateEleve(UpdateView):
    model = Eleve
    fields = ['nom', 'prenom', 'chambre', 'classe', 'annee', 'mail']

    def get_success_url(self):
        return reverse('eleve', args = [self.object.id])

class UpdateMachine(UpdateView):
    model = Machine
    fields = ['mac', 'type' , 'actif']

    def get_success_url(self):
        return reverse('eleves')

class CreateEleve(CreateView):
    model = Eleve
    fields = ['nom', 'prenom', 'chambre', 'classe', 'annee', 'mail']
    def get_success_url(self):
        return reverse('eleve', args = [self.object.id])

class CreateMachine(CreateView):
    model = Machine
    fields = ['mac', 'type' , 'actif']

    def form_valid(self, form):
        form.instance.eleve=Eleve.objects.get(id=self.kwargs['eleve'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nom']= Eleve.objects.get(id=self.kwargs['eleve'])
        return context



    def get_success_url(self):
        return reverse('eleves')

class DeleteMachine(DeleteView):
    template_name = "wifi/eleve_confirm_delete.html"
    model = Machine
    def get_success_url(self):
        return reverse('eleves')

class DeleteEleve(DeleteView):
    model = Eleve
    def get_success_url(self):
        return reverse('eleves')

def update_wifi(request):
    template="wifi/execute.html"
    child = pexpect.spawn('ssh 192.168.1.40', encoding='utf-8')
#    child.logfile = sys.stdout
    child.expect('User:')
    child.sendline('referent')
    child.expect('Password:')
    child.sendline('Champollion38')
    child.expect('(Cisco Controller).*')
    child.sendline('show macfilter summary')
    child.expect('(Cisco Controller).*')
    mac = child.before

    list_mac_cisco = re.findall(r"([0-9a-f]{2}(?::[0-9a-f]{2}){5})", mac, re.I)

    list_mac_database = Machine.objects.filter(actif=True).values_list('mac')
    list_mac_database = [m[0] for m in list_mac_database]

    # print (list_mac_cisco)
    # print(list_mac_database)

    to_add=[]
    to_delete=[]
    for m in list_mac_database:
        if m not in list_mac_cisco:
            to_add.append(m)

    for m in list_mac_cisco:
        if m not in list_mac_database:
            to_delete.append(m)

    for m in to_add:
        cmd = "config macfilter add " + m + " 0"
        child.sendline(cmd)
        child.expect('(Cisco Controller).*')
        # print(child.before)

    for m in to_delete:
        cmd = "config macfilter delete " + m
        child.sendline(cmd)
        child.expect('(Cisco Controller).*')
        # print(child.before)

    child.close()

    context={}
    context['add']=to_add
    context['del']=to_delete

    return render(request, template, context)