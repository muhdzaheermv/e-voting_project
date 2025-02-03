from django.shortcuts import render,redirect,get_object_or_404
from . models import VoterReg,ElectionOfficerReg,Election,Candidate,Vote,EligibleVoter,ElectionManager,PresidingOfficer
from django.contrib import messages
from django.http import HttpResponse
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
      return render(request,'officer_home.html')
   else:
      return render(request,'register.html')
  
# def login(request):
#    if request.method=='POST':
#       uname = request.POST.get('runame')
#       passw = request.POST.get('rpass')
#       cr = VoterReg.objects.filter(username=uname,password=passw)
#       if cr:
#          details = VoterReg.objects.get(username=uname, password = passw)
#          username = details.username
#          request.session['cs']=username

#          return render(request,'home.html')
#       else:
#          message="Invalid Username Or Password"
#          return render(request,'login.html',{'me':message})
#    else: 
#       return render(request,'login.html')
  
def login(request):
   if request.method=='POST':
      uname = request.POST.get('runame')
      cr = VoterReg.objects.filter(username=uname)
      if cr:
         details = VoterReg.objects.get(username=uname)
         username = details.username
         request.session['cs']=username

         return render(request,'available_elections.html')
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
      return render(request,'manager_dashboard.html')
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
  

  
# views.py
def create_election(request):
    officer_id = request.session.get('lcu')  # Get the officer's ID from the session

    if request.method == 'POST':
        election_no = request.POST.get('relection_no')
        fname = request.POST.get('rfname')
        start_time = request.POST.get('rstime')
        end_time = request.POST.get('retime')
        description = request.POST.get('rdescription')
        status = request.POST.get('rstatus')

        # Check if the election number already exists
        if Election.objects.filter(election_no=election_no).exists():
            messages.error(request, 'Election number already exists. Please choose a different one.')
            return render(request, 'create_election.html')

        # Get the officer from the session and create the election
        officer = ElectionOfficerReg.objects.get(id_no=officer_id)
        Election.objects.create(
            election_officer=officer,  # Link the election to the officer
            election_no=election_no,
            name=fname,
            start_time=start_time,
            end_time=end_time,
            description=description,
            status=status
        )

        messages.success(request, 'Election created successfully!')
        return redirect('officer_home')  # Redirect to officer home page

    return render(request, 'create_election.html')

  
def election_list(request):
    data=Election.objects.all()
    d=Candidate.objects.all()
    election = Election.objects.all()
    candidates = Candidate.objects.all()
    return render(request,'election_list.html',{"data":data,'d':d,'election':election,'candidates': candidates})

def voters_list(request):
    data=VoterReg.objects.all()
    return render(request,'voters_list.html',{"data":data})

def create_candidate(request, election_id):
    election = Election.objects.get(id=election_id)  # Retrieve the election
    if request.method == 'POST':
        name = request.POST.get('rname')
        profile_picture = request.FILES.get('rprofile_picture')
        description = request.POST.get('rdescription')
        subname = request.POST.get('rsubname')

        Candidate(election=election, name=name, profile_picture=profile_picture, description=description, subname=subname).save()
        messages.success(request, 'Candidate created successfully!')
        return redirect('officer_home') 
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
        messages.success(request, 'Candidate updated successfully!')
        return redirect('officer_home') 
    else:
        return render(request, 'edit_candidate.html', {'candidate': candidate})

def delete_candidate(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)  # Retrieve the candidate
    candidate.delete()
    messages.success(request, 'Candidate deleted successfully!')
    return redirect('officer_home') 

def delete_election(request, election_id):
    try:
        election = Election.objects.get(id=election_id)
        # Optionally, delete related candidates
        election.candidates.all().delete()
        election.delete()
        messages.success(request, 'election deleted successfully!')
        return redirect('officer_home') 
    except Election.DoesNotExist:
        return render(request, 'officer_home.html', {'message': 'Election not found!'})
    
def election_detail(request, election_id):
    try:
        election = Election.objects.get(id=election_id)
        return render(request, 'election_detail.html', {'election': election})
    except Election.DoesNotExist:
        return render(request, '404.html', {'message': 'Election not found.'})
    
def election_detail_manager(request, election_id):
    try:
        election = Election.objects.get(id=election_id)
        return render(request, 'election_detail_manager.html', {'election': election})
    except Election.DoesNotExist:
        return render(request, '404.html', {'message': 'Election not found.'})
    

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
    voter_username = request.session.get('cs')
    if not voter_username:
        return redirect('login')

    elections = Election.objects.all()  # Fetch all elections

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
    officer_id = request.session.get('lcu')
    officer = ElectionOfficerReg.objects.get(id_no=officer_id)

    # Get elections created by the officer
    elections = officer.elections.all()

    return render(request, 'officer_home.html', {'elections': elections})

def manager_dashboard(request):
    if 'manager_id' not in request.session:
        return redirect('login_election_manager') 
    
    officer_id = request.session.get('lcu')
    officer = ElectionOfficerReg.objects.get(id_no=officer_id)

    # Get elections created by the officer
    elections = officer.elections.all()
# Redirect if not logged in

    # Fetch all Election Officers
    officers = ElectionOfficerReg.objects.all()

    return render(request, 'manager_dashboard.html', {'officers': officers,'elections': elections})



def register_manager(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        username = request.POST['username']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']  # Normally, this should be hashed

        # Ensure username and email are unique
        if ElectionManager.objects.filter(username=username).exists():
            return HttpResponse("Username already taken.")
        if ElectionManager.objects.filter(email=email).exists():
            return HttpResponse("Email already in use.")

        # Create Election Manager
        ElectionManager.objects.create(
            fullname=fullname,
            username=username,
            phone_number=phone_number,
            email=email,
            password=password  # Storing password as plain text (not recommended for real-world applications)
        )

        return redirect('login_manager')  # Redirect to login page after successful registration

    return render(request, 'register_manager.html')  # Show registration form


# Login Election Manager
def login_manager(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if user exists
        try:
            manager = ElectionManager.objects.get(username=username, password=password)
            request.session['manager_id'] = manager.id  # Save session
            return redirect('manager_dashboard')
        except ElectionManager.DoesNotExist:
            return HttpResponse("Invalid login credentials")

    return render(request, 'login_manager.html')


# Election Manager Dashboard (Only accessible after login)





def register_presiding_officer(request):
    if request.method == 'POST':
        officer_id = request.POST['officer_id']
        fullname = request.POST['fullname']
        username = request.POST['username']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']  # Storing as plain text (not secure, but per requirement)

        # Check for duplicate officer ID, username, or email
        if PresidingOfficer.objects.filter(officer_id=officer_id).exists():
            return HttpResponse("Officer ID already taken.")
        if PresidingOfficer.objects.filter(username=username).exists():
            return HttpResponse("Username already taken.")
        if PresidingOfficer.objects.filter(email=email).exists():
            return HttpResponse("Email already in use.")

        # Create Presiding Officer
        officer = PresidingOfficer.objects.create(
            officer_id=officer_id,
            fullname=fullname,
            username=username,
            phone_number=phone_number,
            email=email,
            password=password
        )

        # Redirect to login after successful registration
        return redirect('officer_home')

    return render(request, 'register_presiding_officer.html')  # Show registration form

def login_presiding_officer(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            officer = PresidingOfficer.objects.get(username=username, password=password)
            request.session['officer_id'] = officer.id  # Start session
            return redirect('presiding_officer_dashboard')
        except PresidingOfficer.DoesNotExist:
            return HttpResponse("Invalid login credentials")

    return render(request, 'login_presiding_officer.html')




def presiding_officer_dashboard(request):
    if 'officer_id' not in request.session:
        return redirect('login_presiding_officer')  # Redirect if not logged in

    officer = PresidingOfficer.objects.get(id=request.session['officer_id'])

    # Get search query
    query = request.GET.get('q', '')  # Get 'q' parameter from the search form

    # Filter voters based on search input
    if query:
        voters = VoterReg.objects.filter(fullname__icontains=query)  # Case-insensitive search
    else:
        voters = VoterReg.objects.all()  # Show all voters if no search query

    if request.method == 'POST':
        # Verify or deny voter based on their ID
        voter_id = request.POST.get('voter_id')
        action = request.POST.get('action')

        try:
            voter = VoterReg.objects.get(id=voter_id)
            if action == 'verify':
                voter.verified = True
                voter.save()
            elif action == 'deny':
                voter.verified = False
                voter.save()

            return redirect('presiding_officer_dashboard')  # Refresh the page

        except VoterReg.DoesNotExist:
            return HttpResponse("Voter not found")

    return render(request, 'presiding_officer_dashboard.html', {'officer': officer, 'voters': voters, 'query': query})

def voter_verify(request):
    
    voter_username = request.session.get('cs')
    if not voter_username:
        return redirect('login')

    elections = Election.objects.all()
    
    voter_verified = None
    if request.method == 'POST':
        voter_input = request.POST['voter_input']

        try:
            # Try finding the voter by username or email
            voter = VoterReg.objects.get(username=voter_input) or VoterReg.objects.get(email=voter_input)
            voter_verified = voter.verified  # Store verification status

        except VoterReg.DoesNotExist:
            voter_verified = False  # If no such voter found

    return render(request, 'voter_verify.html', {'voter_verified': voter_verified,'elections': elections})
