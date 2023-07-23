from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
def registration(request):
    d={'usfo':UserForm(),'pfo':ProfileForm()}
    if request.method=='POST' and request.FILES:
        usfd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if usfd.is_valid() and pfd.is_valid():
            nsufo=usfd.save(commit=False)
            submittedpw=usfd.cleaned_data['password']
            nsufo.set_password(submittedpw)
            nsufo.save()

            nspo=pfd.save(commit=False)
            nspo.username=nsufo
            nspo.save()

            send_mail('Registration',
                      'registration is successfull',
                      'sinchanagr2@gmail.com',
                      [nsufo.email]
                      ,fail_silently=True)
            
        return HttpResponse('registration is successfull')



    return render(request,'registration.html',d)



def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')


def userlogin(request):
   
    if request.method=='POST':
         username=request.POST['username']
         password=request.POST['password']
         
         AUO=authenticate(username=username,password=password)
         if AUO:
             if AUO.is_active:
                 login(request,AUO)
                 request.session['username']=username
                 return HttpResponseRedirect(reverse('home'))
             else:
                 return HttpResponse('not a active user')
         else:
           return HttpResponse('invalid details')
    return render(request,'userlogin.html')

@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))