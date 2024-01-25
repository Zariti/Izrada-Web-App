from django.shortcuts import render, redirect #doda sam redirect
from .models import Korisnik, Predmeti, Upisi
from .forms import KorisnikForm, PredmetiForm
from django.http import HttpResponseNotAllowed, HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.views import LoginView # ovo je importan view u obliku klase kojeg cemo malo izminit
from .forms import PredmetProfesoruForm

from django.urls import reverse  #za vise opcija prilikom redirect-a -> redirect(reverse(..., args[..]))
from django.contrib.auth.decorators import login_required

#@login_required -> vraca nas na login page ako nismo logirani

# Create your views here.

#GET - kad udemo na stranicu priko linka ili url(prvi put)
#POST - kad kliknemo submit button (podaci se salju)

#view povlaci iz forme, a forma povlaci iz modela

#ovo je view isto, viewovi mogu biti u obliku klasa takodjer
class UpdatedLoginView(LoginView): #nasljeduje LoginView
    def get_success_url(self):
        user_id = self.request.user.id #uzima id logiranog korisnika kojeg salje na home
        return f'/home/{user_id}'
    
#ovoj funkciji cemo imat pristup samo ako smo admin!!
@login_required
def dodaj_korisnika(request):
    if request.method == 'GET':
        form = KorisnikForm()
        return render(request, 'dodaj_korisnika.html', {'form': form})
    elif request.method == 'POST':
        form = KorisnikForm(request.POST)
        if form.is_valid():
            #print(form.cleaned_data.get('password'))
            form.save()
            return redirect('dodajKorisnika')
        else:
            return HttpResponseNotAllowed()
####


#### STUDENTI
@login_required
def studenti_lista(request):
    studenti = Korisnik.objects.filter(role="stu")

    user_id = request.user.id  #ovo je za link da se mozemo vratit na home page od logiranog usera
    return render(request, 'studenti_lista.html', {'studenti': studenti, 'user_id': user_id})

@login_required
def dodaj_studenta(request):
    if request.method == 'GET':
        form = KorisnikForm()

    elif request.method == 'POST':
        form = KorisnikForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            if role != 'stu':
                form.add_error('role', 'Samo se student moze dodati!')
                #return render(request, 'dodaj_studenta.html', {'form': form})
            else:
                form.save()
                return redirect('studentiLista')
    return render(request, 'dodaj_studenta.html', {'form': form})

@login_required
def edit_studenta(request, user_id):
    student = Korisnik.objects.get(pk=user_id) #uzima pravog korisnika
    if request.method == 'GET':
        form = KorisnikForm(instance=student)
        return render(request, 'edit_student.html', {'form': form})
    elif request.method == 'POST':
        form = KorisnikForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('studentiLista') #ako stisnemo submit vraca nas na listu
#########

#### PROFESORI
@login_required
def profesori_lista(request):
    profesori = Korisnik.objects.filter(role='prof')

    user_id = request.user.id
    return render(request, 'profesori_lista.html', {'profesori': profesori, 'user_id': user_id})

@login_required
def dodaj_profesora(request):
    if request.method == 'GET':
        form = KorisnikForm()
        return render(request, 'dodaj_profesora.html', {'form': form})
    elif request.method == 'POST':
        form = KorisnikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profesoriLista')

@login_required   
def edit_profesora(request, user_id):
    profesor = Korisnik.objects.get(pk=user_id)
    if request.method == 'GET':
        form = KorisnikForm(instance=profesor)
        return render(request, 'edit_profesora.html', {'form': form})
    elif request.method == 'POST':
        form = KorisnikForm(request.POST, instance=profesor)
        if form.is_valid():
            form.save()
            return redirect('profesoriLista')

########

###PREDMETI 

@login_required
def dodaj_predmet(request):
    if request.method == 'GET':
        form = PredmetiForm()
        return render(request, 'dodaj_predmet.html', {'form': form})
    elif request.method == 'POST':
        form = PredmetiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('predmetiLista')
        else:
            return HttpResponseNotAllowed

@login_required
def predmeti_lista(request):
    predmeti = Predmeti.objects.all()

    user_id = request.user.id
    return render(request, 'predmeti_lista.html', {'predmeti': predmeti, 'user_id': user_id})

@login_required
def edit_predmeta(request, predmet_id):
    predmet = Predmeti.objects.get(pk=predmet_id)
    if request.method == 'GET':
        form = PredmetiForm(instance=predmet)
        return render(request, 'edit_predmeta.html', {'form': form})
    elif request.method == 'POST':
        form = PredmetiForm(request.POST, instance=predmet)
        if form.is_valid():
            form.save()
            return redirect('predmetiLista')

@login_required
def predmet_profesoru(request): #posto koristimo formu obicno a ne modelformu triba drukcije koristit form.save jer je u modelform automatizirano
    if request.method == 'GET':
        form = PredmetProfesoruForm()
        return render(request, 'predmet_profesoru.html', {'form': form})
    elif request.method == 'POST':
        form = PredmetProfesoruForm(request.POST)
        if form.is_valid():
            #form.save()
            predmet = form.cleaned_data['predmet']
            profesor = form.cleaned_data['profesor']
            

            predmet.nositelj = profesor
            predmet.save()
            return redirect('dajPredmetProfesoru')
    else:
        return HttpResponseNotAllowed

@login_required
def predmeti_od_profesora(request, user_id):
    profesorovi_predmeti = Predmeti.objects.filter(nositelj_id=user_id)
    return render(request, 'predmeti_od_profesora.html', {'predmeti': profesorovi_predmeti, 'user_id': user_id})

@login_required
def studenti_na_predmetu(request, predmet_id):
    upisi_sa_predmetom = Upisi.objects.filter(predmet=predmet_id)
    studenti_sa_predmetom = [upis.student for upis in upisi_sa_predmetom] #ovi id-evi su strani kljucevi stoga osim samog broja takoder predtsavljaju cili objekt
    #studenti_sa_predmetom_objekti = Korisnik.objects.filter(id__in=studenti_sa_predmetom) #id__in zato jer ih je vise u listi
    predmet_objekt = Predmeti.objects.get(pk=predmet_id) #kako bi dobavili ime etc..

    user_id = request.user.id #nacin za dohvacanje usera koji je logiran trenutno!!
    return render(request, 'studenti_na_predmetu.html', {'predmet': predmet_objekt, 'studenti_objekti': studenti_sa_predmetom, 'user_id': user_id})
##########

@login_required
def home_page(request, user_id):
    user = Korisnik.objects.get(id=user_id)
    return render(request, 'home.html', {'username': user.username, 'role': user.role, 'user_id': user_id})

@login_required
def upisni_list(request, user_id): #ovde je user_id korisnika 
    student = Korisnik.objects.get(pk=user_id) #trazi se student
    upisani_predmeti = Upisi.objects.filter(student=student).values_list('predmet', flat=True) #ovo koristimo samo da nademo neupisane
    neupisani_predmeti = Predmeti.objects.exclude(id__in=upisani_predmeti) #id__in= ako se oce dohvatiti vise id-eva, a id= ako samo 1
    #ovo iznad su objekti predmeta koji nisu upisani

    upisani_predmeti_iz_Predmeti = Predmeti.objects.filter(id__in=upisani_predmeti) #a ovaj cemo koristit kao kontekst kako bi mogli uzet id od predmeta
    upisani_predmeti_sve = Upisi.objects.filter(student=student)

    polozeni_predmeti = Upisi.objects.filter(student=student, status="polozen").values_list('predmet_id', flat=True) 
    nepolozeni_predmeti = Upisi.objects.filter(student=student, status="izg_potpis").values_list('predmet_id', flat=True)
    #svejedno je jeli u values_list koristis naziv 'predmet_id' iz tablice ili naziv 'predmet' iz modela! 


    user_id_logirani = request.user.id #id logiranog usera kako bi se moga vratit u home i kako bi se vidile ovlasti, ovo saljemo u context
    user_obj_logirani = Korisnik.objects.get(id=user_id_logirani) #kako bi mogli vidit role tkd nam prikaze pravi 'natrag na home'

    return render(request, 'upisni_list.html', {'neupisani_predmeti': neupisani_predmeti, 'upisani_predmeti': upisani_predmeti_iz_Predmeti, 
    'user_id': user_id, 'student': student, 'user_obj_logirani': user_obj_logirani, 'upisani_predmeti_sve': upisani_predmeti_sve, 
    'polozeni_predmeti': polozeni_predmeti, 'nepolozeni_predmeti': nepolozeni_predmeti})

from django.db.models import Q

#Item.objects.filter(Q(creator=owner) | Q(moderated=False))
#  SA ISPITA ZADATAK KOJI RADI !
#def upisi_predmet(request, user_id, predmet_id):
#    student = Korisnik.objects.get(pk=user_id)
#    predmet = Predmeti.objects.get(pk=predmet_id)
#    upisi_studenta = Upisi.objects.filter(student=student)  #OVDE SAN FALIOOOOO!!! ja stavio predmet isto kao uvjet 
#    if student.status == 'red':
#        upisi_studenta_prva_god = upisi_studenta.filter(Q(predmet__sem_red=1) | Q(predmet__sem_red=2)) #svi predmeti iz prve god
#        if upisi_studenta_prva_god.filter(Q(status="izg_potpis") | Q(status="upisan")).exists():
#            predmeti_trece = Predmeti.objects.filter(sem_red__in=[5,6]).values_list("id", flat=True) #I OVDE ISTOOOOO!!!
#            if predmet_id in predmeti_trece:
#                return HttpResponse("Nisi polozio sve potrebne predmete za taj upis")
#                #return redirect('upisniList', user_id=user_id)
#            else:
#                Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#                #return render(request, 'upisniList.html', {'predmet_id': predmet_id, 'predmeti_trece': predmeti_trece})
#                return redirect('upisniList', user_id=user_id)
#                
#        else:
#            Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#            #return render(request, 'upisniList.html', {'predmet_id': predmet_id, 'predmeti_trece': predmeti_trece})
#            return redirect('upisniList', user_id=user_id)
#    elif student.status == 'izv':
#        upisi_studenta_prva_god = upisi_studenta.filter(Q(predmet__sem_izv=1) | Q(predmet__sem_izv=2)) #svi predmeti iz prve god
#        upisi_studenta_druga_god = upisi_studenta.filter(Q(predmet__sem_izv=3) | Q(predmet__sem_izv=4))
#        if upisi_studenta_prva_god.filter(Q(status="izg_potpis") | Q(status="upisan")).exists():
#            predmeti_cetvrte = Predmeti.objects.filter(Q(sem_izv=7) | Q(sem_izv=8)).values_list("predmet_id", flat=True)
#            if predmet_id in predmeti_cetvrte:
#                #return HttpResponse("Nisi polozio sve potrebne predmete za taj upis")
#                return redirect('upisniList', user_id=user_id)
#            
#            else:
#                Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#                return redirect('upisniList', user_id=user_id)
#        elif upisi_studenta_druga_god.filter(Q(status="izg_potpis") | Q(status="upisan")).exists():
#            predmeti_cetvrte = Predmeti.objects.filter(Q(sem_izv=7) | Q(sem_izv=8)).values_list("predmet_id", flat=True)
#            if predmet_id in predmeti_cetvrte:
#                #return HttpResponse("Nisi polozio sve potrebne predmete za taj upis")
#                return redirect('upisniList', user_id=user_id)
#            
#            else:
#                Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#                return redirect('upisniList', user_id=user_id)
#        
#    else:
#        #Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#        return redirect('upisniList', user_id=user_id)
    
    #return HttpResponse("Nisi polozio sve potrebne predmete za taj upis")

#def upisi_predmet(request, user_id, predmet_id):
#    student = Korisnik.objects.get(id=user_id)
#    predmet = Predmeti.objects.get(id=predmet_id)
#    upisani_predmeti = Upisi.objects.filter(student=student).values("predmet_id")
#    #upisani_predmeti_obj = Predmeti.objects.filter(id__in=upisani_predmeti)#.values_list("id", flat=True)
#    print("Predmet koji san klika: ", predmet_id)
#    if student.status == "red":
#        upisani_predmeti_trece = upisani_predmeti.filter(predmet__sem_red__in=[5,6])#.values_list("predmet_id", flat=True)
#        #upisani_predmeti_trece_obj_izb = upisani_predmeti_obj.filter(sem_red__in=[5,6], izborni="da").values_list("id", flat=True)
#        neupisani_predmeti = Predmeti.objects.exclude(id__in=upisani_predmeti)
#        
#        #print(upisani_predmeti_trece_obj_izb)
#        upisani_predmeti_trece_izb = upisani_predmeti_trece.filter(predmet__izborni="da").values_list("predmet_id", flat=True).distinct()
#        if predmet.izborni == 'da' and (predmet.sem_red == 5 or predmet.sem_red == 6): # NEMOJ ZABORAVIT ZAGRADE OVDE!!!
#        #if upisani_predmeti_trece_obj_izb.filter(id=predmet_id).exists():
#            #if len(upisani_predmeti_trece_obj_izb) >= 2: #znaci vec imaju dva upisana
#            if len(upisani_predmeti_trece_izb) >= 2:
#                return HttpResponse("Ne moze vise od dva izborna")
#            else:
#                Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#                return redirect('upisniList', user_id=user_id)
#        else:
#            Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#            #return HttpResponse("Cudno")
#            return redirect('upisniList', user_id=user_id)
#        
#    if student.status == "izv":
#        upisani_predmeti_cetvrte = upisani_predmeti.filter(predmet__sem_izv__in=[7,8])
#        upisani_predmeti_cetvrte_izb = upisani_predmeti_cetvrte.filter(predmet__izborni="da").values_list("predmet_id", flat=True).distinct()
#        if predmet.izborni == "da" and (predmet.sem_izv == 7 or predmet.sem_izv == 8):  # NEMOJ ZABORAVIT ZAGRADE OVDE!!
#            if len(upisani_predmeti_cetvrte_izb) >= 1: #znaci vec ima jedan upisan izborni
#                return HttpResponse("Ne moze vise od jednog izbornog")
#            else:
#                Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#                return redirect("upisniList", user_id=user_id)
#        else:
#            Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#            return redirect("upisniList", user_id=user_id)
#    else:
#        return HttpResponse("Negdje je nastala greska, provjeri kod")

from django.db.models import Count
##  ZA VJEZBU 
def broj_izv_red(request):
    upisi = Upisi.objects.filter(status="polozen")
    upisi_izv = upisi.filter(student__status="izv").values("student_id").annotate(br_pol=Count("student_id")).filter(br_pol__gt=3).distinct().count()
    upisi_red = upisi.filter(student__status="red").count()
    return render(request ,"z_broj_izv_red.html", {'br_izv': upisi_izv, 'br_red': upisi_red})

#def upisi_predmet(request, user_id, predmet_id):
#    student = Korisnik.objects.get(id=user_id)
#    predmet = Predmeti.objects.get(id=predmet_id)
#    izgubljeni_pr = Upisi.objects.filter(student=student, status="izg_potpis").count()
#    if izgubljeni_pr >= 4:
#        return redirect('upisniList', user_id=user_id)
#    else:
#        Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#        return redirect('upisniList', user_id=user_id)

# Napravit da za svakog redovnog studenta izbroji koliko je predmeta koja imaju vise od 4 ectsa polozio i da
# za svakog izvanrednog studenta izbroji kolko je polozio predmeta koja imaju vise od 3 ectsa 
def br_pol_4_3(request, user_id):
    student = Korisnik.objects.get(id=user_id)
    upisi_studenta = Upisi.objects.filter(student=student)
    upisi_studenta_polozeni = upisi_studenta.filter(status="polozen") 
    if student.status == "red":
        br_predmeta_gt_4_ects = upisi_studenta_polozeni.filter(predmet__ects__gt=4).count()
        return render(request, 'z_br_pol_43ects.html', {'br_predmeta': br_predmeta_gt_4_ects})
    elif student.status == "izv":
        br_predmeta_gt_3_ects = upisi_studenta_polozeni.filter(predmet__ects__gt=3).count()
        return render(request, 'z_br_pol_43ects.html', {'br_predmeta': br_predmeta_gt_3_ects})
    else:
        return HttpResponse("nesto nije uredu!")

def najtezi_predmet_gt_4(request):
    #predmeti = Predmeti.objects.all()
    upisi = Upisi.objects.filter(status="izg_potpis", predmet__ects__gt=4).values_list("predmet_id", flat=True).annotate(broj=Count("predmet_id")).order_by("-broj")
    #print(upisi)
    najgori_id = upisi[0]
    najgori_obj = Predmeti.objects.get(id=najgori_id)
    #print(najgori_id)

    return render(request, 'z_najtezi_predmet_gt_4.html', {'najtezi_predmet':najgori_obj})
    
# IZBROJAT SVE STUDENTE KOJI SU POLOZILI BAR 4 PREDMETA I CIJE IME POCINJE SA 'M'
def stud_sa_m(request):
    upisi = Upisi.objects.filter(status='polozen', student__username__istartswith='M').values_list('student_id', flat=True).annotate(br_pol=Count('student_id')).filter(br_pol__gt=3).values_list('student_id', flat=True)
    studenti = Korisnik.objects.filter(id__in=upisi)
    return render(request, 'z_stud_sa_m.html', {'studenti': studenti})

# Onemoguciti red studentima upis predmeta trece god ako nije polozio sve premete iz prve, i onemogucit izv stud upis predmeta
# cetvrte god ako nije polozio sve predmete iz prve i druge god

#def upisi_predmet(request, user_id, predmet_id):
#    upisi = Upisi.objects.filter(student=user_id)
#    student = Korisnik.objects.get(id=user_id)
#    predmet = Predmeti.objects.get(id=predmet_id)
#    if student.status == "red":
#        if upisi.filter(predmet__sem_red__in=[1,2], status__in=["izg_potpis", "upisan"]).exists():
#            if predmet.sem_red == 5 or predmet.sem_red == 6:
#                return HttpResponse("Nemozes!")
#            else:
#                Upisi.objects.create(predmet=predmet, student=student, status="upisan")
#                return redirect('upisniList', user_id=user_id)
#        else:
#            Upisi.objects.create(predmet=predmet, student=student, status="upisan")
#            return redirect('upisniList', user_id=user_id)
#    if student.status == "izv":
#        if upisi.filter(predmet__sem_izv__in=[1,2,3,4], status__in=["izg_potpis", "upisan"]).exists():
#            if predmet.sem_izv == 7 or predmet.sem_izv == 8:
#                return HttpResponse("Nemozes!")
#            else:
#                Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#                return redirect('upisniList', user_id=user_id)
#        else:
#            Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#            return redirect('upisniList', user_id=user_id)

def stud_na_zadnjoj(request):
    studenti_zadnje = Upisi.objects.filter(predmet__sem_red__in=[5,6,7,8]).values('student_id').distinct().count()
    return render(request, 'z_br_stud_zadnje.html', {'broj': studenti_zadnje})

from django.db.models import Max

#Napravit da ako je redovni student pa 4 ili vise predmeta da nemore vise upisat
#nijedan predmet iz njegove godine. ako je izvanredni te ako je pa vise od 5
#(ili jednako) predmeta da nemore upisat vise ni jedan iz njegove trenutne godine

#def upisi_predmet(request, user_id, predmet_id):
#    student = Korisnik.objects.get(id=user_id)
#    predmet = Predmeti.objects.get(id=predmet_id)
#    upisani_predmeti = Upisi.objects.filter(student=student)
#    if student.status == 'red':
#        najv_sem_predm = upisani_predmeti.values("predmet_id").annotate(max_sem_red=Max("predmet__sem_red")).order_by("-max_sem_red").first() #vraca dict{predmet_id: 4, max_sem_red: 5}
#        najv_predmet_po_sem = Predmeti.objects.get(id=najv_sem_predm['max_sem_red']) #triba extractat ovo tocno!
#        njegov_sem = najv_predmet_po_sem # ovo je njegov semestar trenutni
#        #Hardcoding
#        if njegov_sem == 1 or njegov_sem == 2:
#            njegova_god = 1
#        elif njegov_sem == 3 or njegov_sem == 4:
#            njegova_god = 2
#        else:
#            njegova_god = 3
#        
#        if predmet.sem_red == 1 or predmet.sem_red == 2:
#            predmeta_god = 1
#        elif predmet.sem_red == 3 or predmet.sem_red == 4:
#            predmeta_god = 2
#        else:
#            predmeta_god = 3

#        br_izg_predmeta = upisani_predmeti.filter(status="izg_potpis").count()
#        if br_izg_predmeta >= 4:
#            if predmeta_god == njegova_god:
#                return HttpResponse("ne mozes!")
#            else:
#                Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#                return redirect('upisniList', user_id=user_id)
#        else:
#            Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#            return redirect('upisniList', user_id=user_id)
#    if student.status == "izv":
#        br_izg_predmeta = upisani_predmeti.filter(status="izg_potpis").count()
#        njegov_sem = upisani_predmeti.values("predmet_id").annotate(max_sem_izv=Max("predmet__sem_izv")).order_by("-max_sem_izv").first()
#        njegov_sem = njegov_sem['max_sem_izv']
#        # HC
#        if njegov_sem == 1 or njegov_sem == 2:
#            njegova_god = 1
#        elif njegov_sem == 3 or njegov_sem == 4:
#            njegova_god = 2
#        elif njegov_sem == 5 or njegov_sem == 6:
#            njegova_god = 3
#        else:
#            njegova_god = 4
#        
#        if predmet.sem_izv == 1 or predmet.sem_izv == 2:
#            predmeta_god = 1
#        elif predmet.sem_izv == 3 or predmet.sem_izv == 4:
#            predmeta_god = 2
#        elif predmet.sem_izv == 5 or predmet.sem_izv == 6:
#            predmeta_god = 3
#        else:
#            predmeta_god = 4
#        #
#        if br_izg_predmeta >= 5:
#            if njegova_god == predmeta_god or njegova_god <= predmeta_god:  
#                return HttpResponse("ne mozes!")
#            else:
#                
#                Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#                return redirect('upisniList', user_id=user_id)
#        else:
#            print("nes nije uredu")
#            Upisi.objects.create(student=student, predmet=predmet, status="upisan")
#            return redirect('upisniList', user_id=user_id)


#Pokraj svakog upisanog predmeta na upisnom listu dodat link koji ce prikazivat kolko je studenata polozilo taj predmet
#kolko je upisalo i kolko je izgubilo potpis

def stats(request, predmet_id):
    predmet = Predmeti.objects.get(id=predmet_id)
    studenti_predmeta = Upisi.objects.filter(predmet=predmet)
    br_pol_studenata_predmeta_red = studenti_predmeta.filter(status="polozen", student__status="red").count()
    br_nepol_studenata_predmeta_red = studenti_predmeta.filter(status="izg_potpis", student__status="red").count()
    br_up_studenata_predmeta_red = studenti_predmeta.filter(status="upisan", student__status="red").count()

    br_pol_studenata_predmeta_izv = studenti_predmeta.filter(status="polozen", student__status="izv").count()
    br_nepol_studenata_predmeta_izv = studenti_predmeta.filter(status="izg_potpis", student__status="izv").count()
    br_up_studenata_predmeta_izv = studenti_predmeta.filter(status="upisan", student__status="izv").count()

    return render(request, "z_stats.html", {"br_red_pol": br_pol_studenata_predmeta_red, "br_red_nepol":br_nepol_studenata_predmeta_red, "br_red_up": br_up_studenata_predmeta_red,
                                            "br_izv_pol": br_pol_studenata_predmeta_izv, "br_izv_nepol":br_nepol_studenata_predmeta_izv, "br_izv_up": br_up_studenata_predmeta_izv})


#Napravit program koji ce ispisat sve redovne studente koji su polozili vise od dva predmeta druge godine.

def red_2_god(request):
    studenti = Upisi.objects.filter(student__status="red", predmet__sem_red__in=[3,4], status="polozen")#.values('student_id').annotate(broj=Count('student_id')).filter(broj__gt=2).values_list('student_id', flat=True)
    #studenti_obj = Korisnik.objects.filter(id__in=studenti)
    lst = []
    for upis in studenti:
        broj = studenti.filter(student=upis.student).count()
        if broj > 2:
            if upis.student not in lst:
                lst.append(upis.student)
    #return render(request, 'z_red_2_god.html', {'studenti': studenti_obj})
    studenti_obj = Korisnik.objects.filter(username__in=lst)
    return render(request, 'z_red_2_god.html', {'studenti': studenti_obj})


#Napravit da izbroji sve studente koji su redovni i koji su polozili bar 3 predmeta koja nose vise od 4 boda. 
#I neka izbroji sve izvanredne studente koji su polozili vise od 2 predmeta koji nose vise od 3 boda.

def izbroji_stud(request):
    upisi_red = Upisi.objects.filter(status="polozen", predmet__ects__gt=4, student__status="red")
    upisi_izv = Upisi.objects.filter(status="polozen", predmet__ects__gt=3, student__status="izv")
    lst_red = []
    lst_izv = []
    for upis in upisi_red:
        broj = upisi_red.filter(student=upis.student).count()
        if broj >= 3:
            if upis.student not in lst_red: 
                lst_red.append(upis.student)
    for upis in upisi_izv:
        broj = upisi_izv.filter(student=upis.student).count()
        if broj > 2:
            if upis.student not in lst_izv:
                lst_izv.append(upis.student)
    
    return render(request, 'z_izbroji_stud.html', {'lst_red': lst_red, 'lst_izv': lst_izv})


def izbroji_stud2(request):
    studenti_izv = Korisnik.objects.filter(role="stu", status="izv")
    studenti_red = Korisnik.objects.filter(role="stu", status="red")
    lst_izv = []
    lst_red = []
    for stud in studenti_izv:
        br_izv = Upisi.objects.filter(status="polozen", predmet__ects__gt=3, student=stud).count()
        if br_izv > 2:
            lst_izv.append(stud)
    for stud in studenti_red:
        br_red = Upisi.objects.filter(status="polozen", predmet__ects__gt=4, student=stud).count()
        if br_red > 3:
            lst_red.append(stud)
    
    return render(request, 'z_izbroji_stud.html', {'lst_red': lst_red, 'lst_izv': lst_izv})

#Napravit novu stranicu na kojoj je lista svih predmeta, ukupan broj studenata koji su polozili taj predmet,
#broj redovnih studenata i broj izvanrednih studenata koji su polozili taj predmet. 
#npr. Linearna algebra | Polozeno: 10 | Redovnih: 7 | Izvanrednih: 3

def predmeti_ext(request):
    predmeti = Predmeti.objects.all()
    data = []
    for predmet in predmeti:
        br_ukupno_polozenih = Upisi.objects.filter(predmet=predmet, status="polozen").count()
        br_red_polozenih = Upisi.objects.filter(predmet=predmet, student__status="red", status="polozen").count()
        br_izv_polozenih = Upisi.objects.filter(predmet=predmet, student__status="izv", status="polozen").count()
        data.append({'predmet': predmet, 'br_ukupno_polozenih': br_ukupno_polozenih, 'br_red_polozenih': br_red_polozenih, 'br_izv_polozenih': br_izv_polozenih})
    
    return render(request, 'z_predmeti_ext.html', {'data': data})

def detalji_ext(request, predmet_id):
    predmet = Predmeti.objects.filter(id=predmet_id)
    upisi = Upisi.objects.filter(predmet=predmet, status="polozen")
    upisi_red = upisi.filter(student__status="red").values_list("student_id", flat=True)
    upisi_izv = upisi.filter(student__status="izv").values_list("student_id", flat=True)

    upisi_red_obj = Korisnik.objects.filter(id__in=upisi_red)
    upisi_izv_obj = Korisnik.objects.filter(id__in=upisi_izv)
    return render(request, 'z_detalji_ext.html', {'redovni': upisi_red_obj, 'izvanredni': upisi_izv_obj})


    



@login_required
def upisi_predmet(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmeti.objects.get(pk=predmet_id)
    #if Upisi.objects.filter(student=user_id, predmet=predmet_id).exists():


    Upisi.objects.create(student=student, predmet=predmet, status="upisan")
    #return redirect(reverse('upisniList', args=[user_id])) #ide na path upisni_list/<user_id>
    return redirect('upisniList', user_id=user_id)
    #return render(request, 'upisni_list.html', {'user_id': user_id, 'predmet_id': predmet_id})

@login_required
def ukloni_predmet(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmeti.objects.get(pk=predmet_id)

    upisani = Upisi.objects.get(student=student, predmet=predmet)
    upisani.delete()
    return redirect('upisniList', user_id=user_id)

@login_required
def polozio_predmet(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmeti.objects.get(pk=predmet_id)

    upisani = Upisi.objects.get(student=student, predmet=predmet)
    upisani.status = 'polozen'
    upisani.save()
    return redirect('upisniList', user_id=user_id)

@login_required
def izgubio_predmet(request, user_id, predmet_id):
    student = Korisnik.objects.get(pk=user_id)
    predmet = Predmeti.objects.get(pk=predmet_id)

    upisani = Upisi.objects.get(student=student, predmet=predmet)
    upisani.status = 'izg_potpis'
    upisani.save()
    return redirect('upisniList', user_id=user_id)

##############

@login_required
def upisni_listovi_adm(request):
    studenti = Korisnik.objects.filter(role='stu')

    user_id = request.user.id #id logiranog usera kako bi se moga vratit u home, ovo saljemo u context
    return render(request, 'upisni_listovi_adm.html', {'studenti': studenti, 'user_id': user_id})

@login_required
def upisni_listovi_prof(request):
    studenti = Korisnik.objects.filter(role='stu')

    user_id = request.user.id
    return render(request, 'upisni_listovi_prof.html', {'studenti': studenti, 'user_id': user_id})

@login_required
def stud_koji_su_upisali(request, predmet_id):
    studenti_id = Upisi.objects.filter(predmet=predmet_id).values('student_id') #id-evi studenata
    studenti_koji_su_upisali = Korisnik.objects.filter(id__in=studenti_id)
    return render(request, 'stud_koji_su_upisali.html', {'studenti': studenti_koji_su_upisali})

@login_required
def stud_koji_su_polozili(request, predmet_id):
    studenti_id = Upisi.objects.filter(predmet=predmet_id, status="polozen").values('student_id')
    studenti_koji_su_polozili = Korisnik.objects.filter(id__in=studenti_id)
    return render(request, 'stud_koji_su_polozili.html', {'studenti': studenti_koji_su_polozili})

@login_required
def stud_koji_su_izg_potp(request, predmet_id):
    studenti_id = Upisi.objects.filter(predmet=predmet_id, status="izg_potpis").values('student_id')
    stud_koji_su_izg_potp = Korisnik.objects.filter(id__in=studenti_id)
    return render(request, 'stud_koji_su_izg_potp.html', {'studenti': stud_koji_su_izg_potp})


#def filtriraj_predmete(request):
#    return render(request, 'Z_filtriraj_predmete.html')
    

def svi_predmeti_preko_x_bod(request, bodovi_ects):
    predmeti = Predmeti.objects.filter(ects=bodovi_ects)
    return render(request, 'Z_svi_predmeti_preko_x_bod.html', {'predmeti': predmeti})

def svi_predmeti_semestra_x(request, semestar):
    user_logirani = request.user.id
    user_logirani_obj = Korisnik.objects.get(id=user_logirani)
    if user_logirani_obj.status == "red":
        predmeti = Predmeti.objects.filter(sem_red=semestar)
        return render(request, 'Z_svi_predmeti_semestra_x.html', {'predmeti': predmeti})
    elif user_logirani_obj.status == "izv":
        predmeti = Predmeti.objects.filter(sem_izv=semestar)
        return render(request, 'Z_svi_predmeti_semestra_x.html', {'predmeti': predmeti})



@login_required
def filtriraj_predmete(request):
    user_logirani = request.user.id
    user_logirani_obj = Korisnik.objects.get(id=user_logirani)
    if user_logirani_obj.status == "red":
        if request.method == 'POST':
            bodovi_ects = request.POST.get('number')
            semestar = request.POST.get('semestar')
            if bodovi_ects and semestar:
                predmeti = Predmeti.objects.filter(ects__gt=bodovi_ects, sem_red=semestar)
                return render(request, 'Z_svi_predmeti_preko_x_bod.html', {'predmeti': predmeti})
            if bodovi_ects:
                predmeti = Predmeti.objects.filter(ects__gt=bodovi_ects)
                return render(request, 'Z_svi_predmeti_preko_x_bod.html', {'predmeti': predmeti})
            if semestar:
                predmeti = Predmeti.objects.filter(sem_red=semestar)
                return render(request, 'Z_svi_predmeti_preko_x_bod.html', {'predmeti': predmeti})
        else:
            return render(request, 'Z_filtriraj_predmete.html')
            
    if user_logirani_obj.status == "izv":
        if request.method == 'POST':
            bodovi_ects = request.POST.get('number')
            semestar = request.POST.get('semestar')
            if bodovi_ects and semestar:
                predmeti = Predmeti.objects.filter(ects__gt=bodovi_ects, sem_izv=semestar)
                return render(request, 'Z_svi_predmeti_preko_x_bod.html', {'predmeti': predmeti})
            if bodovi_ects:
                predmeti = Predmeti.objects.filter(ects__gt=bodovi_ects)
                return render(request, 'Z_svi_predmeti_preko_x_bod.html', {'predmeti': predmeti})
            if semestar:
                predmeti = Predmeti.objects.filter(sem_izv=semestar)
                return render(request, 'Z_svi_predmeti_preko_x_bod.html', {'predmeti': predmeti})
        else:
            return render(request, 'Z_filtriraj_predmete.html')
            
            
            
    else:
        return render(request, 'Z_filtriraj_predmete.html')
    
#Z_filtriraj_predmete.html'







#from django.db.models import Count
#from django.db import models
#def tri_predmeta_cetiri_ects(request):
#        studenti = Upisi.objects.filter(status="polozen", predmet__ects__gt=4).values('student_id').annotate(broj_polozenih=Count('student_id')).filter(broj_polozenih__gt=3).values_list('student_id', flat=True)
#        studenti_obj = Korisnik.objects.filter(id__in=studenti)
#
#        return render(request, 'z_tri_predmeta_cetiri_ects.html', {'studenti': studenti_obj})



#def vise_od_dva(request):
#        studenti = Upisi.objects.filter(status="polozen").values('student_id').annotate(broj_polozenih=Count('student_id')).filter(broj_polozenih__gt=2).values_list('student_id', flat=True)
#        studenti_obj = Korisnik.objects.exclude(id__in=studenti).exclude(role__in=["prof", "adm"])
#
#        #studenti_obj = Korisnik.objects.exclude(id__in=studenti, role__in=["prof", "adm"]) exclude triba razbit ako ima vise uvjeta!!!
#        return render(request, 'z_vise_od_dva.html', {'studenti': studenti_obj})


#def broj_stud_na_predmetu(request, predmet_id):
#    predmet = Predmeti.objects.get(id=predmet_id)
#    broj = Upisi.objects.filter(predmet=predmet).values('student_id').count()
#    #broj = 0
#    #for i in broj_lista:
#    #    broj = broj+1
#    
#    
#    return render(request, 'z_broj_stud_na_predmetu.html', {'broj': broj})
    
#def pali_studenti(request):
#    studenti = Upisi.objects.filter(status="izg_potpis", predmet__ects__gt=10).values('student_id').values_list('student_id', flat=True)
#    studenti_obj = Korisnik.objects.filter(id__in=studenti)
#    return render(request, 'z_Vjezbanje3.html', {'studenti': studenti_obj})

## studente koji su samo upisali 1 predmet (a da ga nisu polozili ni pali)

#def stud_upisali_1_pr(request):
#    studenti = Upisi.objects.filter(status="upisan").values("student_id").annotate(broj_upisanih=Count('student_id')).filter(broj_upisanih=1).values_list('student_id', flat=True)
#    studenti_obj = Korisnik.objects.filter(id__in=studenti)
#    return render(request, 'z_Vjezbanje4.html', {'studenti': studenti_obj})

#def studenti_query(request):
#    studenti = Upisi.objects.filter(status="polozen", predmet__ects__gt=4).values("student_id").annotate(br_upisanih=Count("student_id")).filter(br_upisanih__gte=3).values_list("student_id", flat=True)
#    studenti_obj = Korisnik.objects.filter(id__in=studenti)
#    return render(request, "z_Vjezbanje1.html", {'studenti': studenti_obj}) 

#def status(request, user_id):
#    student = Korisnik.objects.get(id=user_id)
#    return render(request, 'z_status.html', {'student': student})

#def najbolji_student(request):
#    studenti = Upisi.objects.filter(status="polozen").values("student_id").annotate(broj_polozenih=Count("student_id")).order_by("-broj_polozenih").first()
#    student_obj = Korisnik.objects.filter(id=studenti)
#    return render(request)
    
    

    
    

