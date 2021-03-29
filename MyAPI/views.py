from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from . models import Entrymodel
import pickle
import json
import numpy as np
import pandas as pd
from sklearn.externals import joblib
# import joblib
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import keras
from keras import backend as K

# Create your views here.


def home(request):
    return render(request,'MyAPI/home.html')

def create_object(request,inp_list):
    #create obj 
    model=Entrymodel()
    model.firstname=request.POST.get(inp_list[0])
    model.lastname=request.POST.get(inp_list[1])
    model.dependants=int(request.POST.get(inp_list[2]))
    model.applicantincome=int(request.POST.get(inp_list[3]))
    model.coapplicatincome=int(request.POST.get(inp_list[4]))
    model.totalincome=int(request.POST.get(inp_list[3]))+int(request.POST.get(inp_list[4]))
    model.loanamt=int(request.POST.get(inp_list[5]))
    model.loanterm=int(request.POST.get(inp_list[6]))
    model.credithistory=int(request.POST.get(inp_list[7]))
    model.gender=request.POST.get(inp_list[8])
    model.married=request.POST.get(inp_list[9])
    model.graduatededucation=request.POST.get(inp_list[10])
    model.selfemployed=request.POST.get(inp_list[11])
    model.area=request.POST.get(inp_list[12])
    model.user_n=request.user
    model.save()


def is_approved(request,inp_list):
    model=joblib.load('MyAPI/ml_related_models/loan_model.pkl')
    sc=joblib.load('MyAPI/ml_related_models/scale_model.pkl')
    max_th=joblib.load('MyAPI/ml_related_models/maximum_th.pkl')
    dep=int(request.POST.get(inp_list[2]))
    ai=int(request.POST.get(inp_list[3]))
    cai=int(request.POST.get(inp_list[4]))
    la=int(request.POST.get(inp_list[5]))
    lat=int(request.POST.get(inp_list[6]))
    ch=int(request.POST.get(inp_list[7]))
    ti=int(request.POST.get(inp_list[3]))+int(request.POST.get(inp_list[4]))
    if request.POST.get(inp_list[8])=='Male':
        gm=1
        gf=0
    else:
        gm=0
        gf=1
    if request.POST.get(inp_list[9])=='Yes':
        my=1
        mn=0
    else:
        my=0
        mn=1
    if request.POST.get(inp_list[10])=='Graduate':
        g=1
        ng=0
    else:
        g=0
        ng=1
    if request.POST.get(inp_list[11])=='Yes':
        sey=1
        sen=0
    else:
        sey=0
        sen=1
    if request.POST.get(inp_list[12])=='Urban':
        au=1
        ar=0
        asu=0
    elif request.POST.get(inp_list[12])=='Rural':
        au=0
        ar=1
        asu=0
    else:
        au=0
        ar=0
        asu=1
    ip=np.array([dep,ai,cai,la,lat,ch,ti,gf,gm,mn,my,g,ng,sen,sey,ar,asu,au]).reshape(1,18)
    ip_scaled=sc.transform(ip)
    op=model.predict(ip_scaled)
    K.clear_session()
    if(op>max_th):
        return 'Eligable for the loan'
    else:
        return 'Not Eligable for the loan'
    
@login_required(login_url="/accounts/signup")
def approvals(request):
    if request.method=='POST':
        inp_list=['firstname','lastname','dependents','applicantincome',
        'coapplicantincome','loanamt','loanterm','credithistory','gender','married','education',
        'selfemployed','area']
        all_filled=True
        for inp in inp_list:
            if not request.POST.get(inp):
                all_filled=False
        if all_filled==True:
            # all fields are filled
            create_object(request,inp_list) #object creation
            l_s=is_approved(request,inp_list) #loan approved or not
            if l_s=='Eligable for the loan':
                loan_status=2
            else:
                loan_status=0
            name=f"{request.POST.get('firstname')} {request.POST.get('lastname')}"
            return render(request,'MyAPI/output.html',{'loan_status':loan_status,'name':name})
        else:
            #all fields are not filled
            return render(request,'MyAPI/check_loan.html',{'error':'All the fields are required!'})
    else:
        #info not yet given
        return render(request,'MyAPI/check_loan.html')