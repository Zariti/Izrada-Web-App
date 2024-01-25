from django.forms import ModelForm #kljucno za izradu formi
from .models import Predmeti, Korisnik, Upisi #importam svoje modele
from django.contrib.auth.hashers import make_password #za password hashat
from django.contrib.auth.forms import UserCreationForm
from django import forms
class KorisnikForm(ModelForm):
    class Meta:
        model = Korisnik
        fields = ['username' ,'email', 'password', 'role', 'status']
        #fields = '__all__'
    
    def clean_password(self):
        password = make_password(self.cleaned_data.get('password'))
        return password

#__init__ je zapravo konstruktor kojem dajem *args i **kwargs jer nez kolko argumenata ce primit
class PredmetiForm(ModelForm): #nasljeduje iz ModelForm
    def __init__(self, *args, **kwargs):
        super(PredmetiForm, self).__init__(*args, **kwargs)
        self.fields.get('nositelj').queryset = Korisnik.objects.filter(role='prof')

    class Meta:
        model = Predmeti
        fields = '__all__'

class UpisiForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpisiForm, self).__init__(*args, **kwargs)
        self.fields.get('student_id').queryset = Korisnik.objects.filter(role='stu')

    class Meta:
        model = Upisi
        fields = '__all__'

class PredmetProfesoruForm(forms.Form):
    predmet = forms.ModelChoiceField(queryset=Predmeti.objects.all())
    profesor = forms.ModelChoiceField(queryset=Korisnik.objects.filter(role='prof'))





class UpisForm(ModelForm):
    class Meta:
        model = Upisi
        fields = ['predmet', 'status']
