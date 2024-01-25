from django.db import models
from django.contrib.auth.models import AbstractUser #AbstractUser je ekstenzija ili prosirenje default User modela
# Create your models here.

class Korisnik(AbstractUser):  #po defaultu ima __init__ funkc priko koje objekt moze primit vise argumenata
    ROLES = (('prof', 'profesor'), ('stu', 'student'), ('adm', 'admin'))
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    role = models.CharField(max_length=50, choices=ROLES)
    status = models.CharField(max_length=50, choices=STATUS)

class Predmeti(models.Model):  #po defaultu nema __init__ koji prima vise argumenata jer ga nismo naveli
    IZBORNI = (('da', 'da'), ('ne', 'ne'))
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    nositelj = models.ForeignKey(Korisnik, on_delete=models.CASCADE, default=11)
    def __str__(self):
        return self.name

class Upisi(models.Model):
    STATUS = (('upisan', 'Upisao predmet'), ('polozen', 'Polozio predmet'), ('izg_potpis', 'Izgubio potpis'))
    student = models.ForeignKey(Korisnik, on_delete=models.CASCADE) #ako je FK automatski se dodaje _id na kraj atributa u tabl
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS) #neki student ima id 26



    


