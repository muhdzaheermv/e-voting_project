from django.shortcuts import render,redirect,get_object_or_404
from . models import VoterReg,ElectionOfficerReg,Election,Candidate,Vote,EligibleVoter
from django.contrib import messages
from datetime import datetime

# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def guide(request):
    return render(request,'guide.html')

def contact(request):
    return render(request,'contact.html')


def home(request):
    return render(request,'home.html')

def register(request):
   if request.method =='POST':
      fname = request.POST.get('rfname')
      phone = request.POST.get('rcontact')
      email = request.POST.get('remail')
      uname = request.POST.get('runame')
      passw = request.POST.get('rpass')
      VoterReg(fullname=fname,contact=phone,email=email,username=uname,password=passw).save()
      return render(request,'login.html')
   else:
      return render(request,'register.html')
  
def login(request):
   if request.method=='POST':
      uname = request.POST.get('runame')
      passw = request.POST.get('rpass')
      cr = VoterReg.objects.filter(username=uname,password=passw)
      if cr:
         details = VoterReg.objects.get(username=uname, password = passw)
         username = details.username
         request.session['cs']=username

         return render(request,'home.html')
      else:
         message="Invalid Username Or Password"
         return render(request,'login.html',{'me':message})
   else: 
      return render(request,'login.html')
  



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
         
         return redirect('officer_home')
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
    
def election_detail(request, id):
    # Fetch the election by ID
    election = Election.objects.get(election_no=id)

    # Fetch associated candidates
    candidates = Candidate.objects.filter(election=election)

    return render(request, 'election_detail.html', {
        'election': election,
        'candidates': candidates
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

def available_elections(request):
    # Ensure the voter is logged in
    voter_username = request.session.get('cs')
    if not voter_username:
        return redirect('login')

    # Get the voter
    voter = VoterReg.objects.get(username=voter_username)
    
    # Exclude elections where the voter has already voted
    voted_elections = Vote.objects.filter(voter=voter).values_list('election', flat=True)
    elections = Election.objects.exclude(id__in=voted_elections)

    return render(request, 'available_elections.html', {'elections': elections})


def vote(request, election_id):
    # Ensure the voter is logged in
    voter_username = request.session.get('cs')
    if not voter_username:
        return redirect('login')

    # Get the voter and election
    voter = get_object_or_404(VoterReg, username=voter_username)
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)

    # Verify if the voter is eligible
    eligible_voter = EligibleVoter.objects.filter(election=election, phone_number=voter.contact).first()
    if not eligible_voter:
        return render(request, 'vote.html', {
            'election': election,
            'candidates': candidates,
            'message': 'You are not eligible to vote in this election. Please contact the election officer.'
        })

    # Handle vote submission
    if request.method == 'POST':
        candidate_id = request.POST.get('candidate_id')

        try:
            # Ensure the candidate exists and belongs to the given election
            candidate = candidates.get(id=candidate_id)

            # Check if the voter has already voted in this election
            if not Vote.objects.filter(voter=voter, election=election).exists():
                # Save the vote
                Vote(voter=voter, election=election, candidate=candidate).save()
                return render(request, 'home.html', {'message': 'Vote cast successfully!'})

            return render(request, 'vote.html', {
                'election': election,
                'candidates': candidates,
                'message': 'You have already voted in this election.'
            })

        except Candidate.DoesNotExist:
            # If the candidate does not exist, show an error message
            return render(request, 'vote.html', {
                'election': election,
                'candidates': candidates,
                'message': 'Invalid candidate selection. Please try again.'
            })

    return render(request, 'vote.html', {'election': election, 'candidates': candidates})




def logout(request):
    request.session.flush()  # Clear all session data
    return redirect('login')

def election_result(request, election_id):
    # Get the election
    election = get_object_or_404(Election, id=election_id)

    # Get candidates and their vote counts
    candidates = Candidate.objects.filter(election=election)
    results = []

    for candidate in candidates:
        vote_count = Vote.objects.filter(candidate=candidate).count()
        results.append({
            'candidate': candidate,
            'votes': vote_count,
        })

    # Sort results by vote count (descending)
    results = sorted(results, key=lambda x: x['votes'], reverse=True)

    return render(request, 'election_result.html', {
        'election': election,
        'results': results,
    })
    

def voter_list(request, election_id):
    # Get the election
    election = Election.objects.get(id=election_id)

    # Fetch all voters who have voted in this election
    voted_voters = Vote.objects.filter(election=election).select_related('voter')

    # Prepare data to display
    voters_data = []
    for vote in voted_voters:
        voters_data.append({
            'username': vote.voter.username,
            'contact': vote.voter.contact,
            'election': election.name,
        })

    return render(request, 'voter_list.html', {
        'election': election,
        'voters': voters_data,
    })
    


# Add Eligible Voter to Election
def add_eligible_voter(request, election_id):
    election = get_object_or_404(Election, id=election_id)

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Check if the phone number is already eligible for this election
        if EligibleVoter.objects.filter(election=election, phone_number=phone_number).exists():
            message = "This phone number is already eligible to vote in this election."
        else:
            # Add the eligible voter
            EligibleVoter.objects.create(election=election, phone_number=phone_number)
            message = "Eligible voter added successfully!"

        return render(request, 'add_eligible_voter.html', {
            'election': election,
            'message': message
        })

    return render(request, 'add_eligible_voter.html', {'election': election})

# Edit Eligible Voter
def edit_eligible_voter(request, eligible_voter_id):
    eligible_voter = get_object_or_404(EligibleVoter, id=eligible_voter_id)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        # Update phone number
        eligible_voter.phone_number = phone_number
        eligible_voter.save()
        messages.success(request, 'Eligible voter updated successfully!')
        return redirect('election_detail', election_id=eligible_voter.election.id)

    return render(request, 'edit_eligible_voter.html', {'eligible_voter': eligible_voter})

# Delete Eligible Voter
def delete_eligible_voter(request, eligible_voter_id):
    eligible_voter = get_object_or_404(EligibleVoter, id=eligible_voter_id)
    
    if request.method == 'POST':
        eligible_voter.delete()
        messages.success(request, 'Eligible voter deleted successfully!')
        return redirect('election_detail', election_id=eligible_voter.election.id)

    return render(request, 'delete_eligible_voter.html', {'eligible_voter': eligible_voter})

# View to display the list of eligible voters for a specific election
def eligible_voter_list(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    eligible_voters = EligibleVoter.objects.filter(election=election)
    return render(request, 'eligible_voter_list.html', {
        'election': election,
        'eligible_voters': eligible_voters
    })
    
def officer_home(request):
    elections = Election.objects.all()  # Fetch all elections
    return render(request, 'officer_home.html', {'elections': elections})










    

