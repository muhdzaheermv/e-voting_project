from django.shortcuts import render,redirect
from . models import VoterReg,ElectionOfficerReg

# Create your views here.

def index(request):
    return render(request,'index.html')


def home(request):
    return render(request,'home.html')

def register(request):
   if request.method =='POST':
      fname = request.POST.get('rfname')
      phone = request.POST.get('rcontact')
      email = request.POST.get('remail')
      uname = request.POST.get('runame')
      passw = request.POST.get('rpass')
      reg(fullname=fname,contact=phone,email=email,username=uname,password=passw).save()
      return render(request,'login.html')
   else:
      return render(request,'register.html')
  
def login(request):
   if request.method=='POST':
      uname = request.POST.get('runame')
      passw = request.POST.get('rpass')
      cr = reg.objects.filter(username=uname,password=passw)
      if cr:
         details = reg.objects.get(username=uname, password = passw)
         username = details.username
         request.session['cs']=username

         return render(request,'home.html')
      else:
         message="Invalid Username Or Password"
         return render(request,'login.html',{'me':message})
   else: 
      return render(request,'login.html')
  
def officer_home(request):
    return render(request,'officer_home.html')


def officer_register(request):
   if request.method =='POST':
      idno = request.POST.get('ridno')
      fname = request.POST.get('rfname')
      phone = request.POST.get('rcontact')
      email = request.POST.get('remail')
      address = request.POST.get('raddress')
      uname = request.POST.get('runame')
      passw = request.POST.get('rpass')
      ElectionOfficerReg(id_no=idno,fullname=fname,contact=phone,email=email,address=address,username=uname,password=passw).save()
      return render(request,'officer_login.html')
   else:
      return render(request,'officer_register.html')


def officer_login(request):
   if request.method=='POST':
      idno =  request.POST.get('ridno')
      uname = request.POST.get('runame')
      passw = request.POST.get('rpass')
      cr = ElectionOfficerReg.objects.filter(id_no=idno,username=uname,password=passw)
      if cr:
         details = ElectionOfficerReg.objects.get(username=uname, password = passw,id_no=idno)
         username = details.username
         request.session['cs']=username
         idno = details.id_no
         request.session['lcu']=idno
         
         return render(request,'officer_home.html')
      else:
         message="Invalid Username Or Password"
         return render(request,'officer_login.html',{'me':message})
   else: 
      return render(request,'officer_login.html')
