from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Entrymodel(models.Model):
    #(what we get, what to insert)
    GENDER_CHOICES=[
        ('Male','Male'),
        ('Female','Female')
    ]
    GRADUATED_CHOICES=[
        ('Graduate','Graduate'),
        ('Not_Graduate','Not_Graduate')
    ]
    MARRIED_CHOICES=[
        ('Yes','Yes'),
        ('No','No')
    ]
    SELFEMPLOYED_CHOICES=[
        ('Yes','Yes'),
        ('No','No')
    ]
    PROPERTY_CHOICES=[
        ('Rural','Rural'),
        ('Semiurban','Semiurban'),
        ('Urban','Urban')
    ]

    firstname=models.CharField(max_length=15)
    lastname=models.CharField(max_length=15)
    dependants=models.BigIntegerField(default=0)
    applicantincome=models.BigIntegerField(default=0)
    coapplicatincome=models.BigIntegerField(default=0)
    totalincome=models.BigIntegerField(default=0)
    loanamt=models.BigIntegerField(default=0)
    loanterm=models.BigIntegerField(default=0)
    credithistory=models.BigIntegerField(default=0)
    gender=models.CharField(max_length=15, choices=GENDER_CHOICES)
    married=models.CharField(max_length=15, choices=MARRIED_CHOICES)
    graduatededucation=models.CharField(max_length=15, choices=GRADUATED_CHOICES)
    selfemployed=models.CharField(max_length=15, choices=SELFEMPLOYED_CHOICES)
    area=models.CharField(max_length=15, choices=PROPERTY_CHOICES)
    user_n=models.ForeignKey(User,on_delete=models.CASCADE,)

    def __str__(self):
        return '{}, {}'.format(self.lastname, self.firstname)