from django.shortcuts import render,redirect,get_object_or_404
from . models import VoterReg,ElectionOfficerReg,Election,Candidate
from datetime import datetime

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
    data = Election.objects.all()  # Fetch all elections
    return render(request, 'officer_home.html', {'data': data})


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
  
def create_election(request):
   idno=request.session['lcu']
   if request.method =='POST':
      fname = request.POST.get('rfname')
      start_time = request.POST.get('rstime')
      end_time = request.POST.get('retime')
      description = request.POST.get('rdescription')
      status = request.POST.get('rstatus')
      Election(election_no=idno,name=fname,start_time=start_time,end_time=end_time,description=description,status=status).save()
      return render(request,'officer_home.html',{'message': 'Election created successfully!'})
   else:
      return render(request,'create_election.html',{'idno':idno})
  
def election_list(request):
    data=Election.objects.all()
    d=Candidate.objects.all()
    election = Election.objects.all()
    candidates = Candidate.objects.all()
    return render(request,'election_list.html',{"data":data,'d':d,'election':election,'candidates': candidates})

def create_candidate(request, election_id):
    election = Election.objects.get(id=election_id)  # Retrieve the election
    if request.method == 'POST':
        name = request.POST.get('rname')
        profile_picture = request.FILES.get('rprofile_picture')
        description = request.POST.get('rdescription')
        subname = request.POST.get('rsubname')

        Candidate(election=election, name=name, profile_picture=profile_picture, description=description, subname=subname).save()
        return render(request, 'officer_home.html', {'message': 'Candidate created successfully!'})
    else:
        return render(request, 'create_candidate.html', {'election': election})
    
def edit_candidate(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)  # Retrieve the candidate
    if request.method == 'POST':
        candidate.name = request.POST.get('rname')
        if 'rprofile_picture' in request.FILES:
            candidate.profile_picture = request.FILES.get('rprofile_picture')
        candidate.description = request.POST.get('rdescription')
        candidate.subname = request.POST.get('rsubname')
        candidate.save()
        return render(request, 'officer_home.html', {'message': 'Candidate updated successfully!'})
    else:
        return render(request, 'edit_candidate.html', {'candidate': candidate})

def delete_candidate(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)  # Retrieve the candidate
    candidate.delete()
    return render(request, 'officer_home.html', {'message': 'Candidate deleted successfully!'})

def delete_election(request, election_id):
    try:
        election = Election.objects.get(id=election_id)
        # Optionally, delete related candidates
        election.candidates.all().delete()
        election.delete()
        return render(request, 'officer_home.html', {'message': 'Election deleted successfully!'})
    except Election.DoesNotExist:
        return render(request, 'officer_home.html', {'message': 'Election not found!'})
    
def election_details(request, election_id):
    # Get the election based on the election_id
    election = get_object_or_404(Election, id=election_id)
    
    # Optionally, get all candidates associated with this election
    candidates = Candidate.objects.filter(election=election)
    
    return render(request, 'election_detail.html', {
        'election': election,
        'candidates': candidates,
    })
    

def edit_election(request, election_id):
    # Fetch the election object using election_id
    election = get_object_or_404(Election, id=election_id)

    # Check if the request is a POST request (i.e., form submission)
    if request.method == 'POST':
        # Get the updated values from the request
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        status = request.POST.get('status')

        # Update the election object with the new values
        election.name = name
        election.description = description
        election.start_time = start_time
        election.end_time = end_time
        election.status = status
        
        # Save the updated election object to the database
        election.save()

        # Redirect to the election detail page after saving
        return redirect('election_detail', election_id=election.id)

    # If GET request, show the current election details in the form
    return render(request, 'edit_election.html', {'election': election})

def view_candidates(request, election_id):
    # Get the election object based on the election_id
    election = get_object_or_404(Election, id=election_id)
    
    # Get all candidates for the given election
    candidates = Candidate.objects.filter(election=election)
    
    return render(request, 'view_candidates.html', {
        'election': election,
        'candidates': candidates,
    })


    

