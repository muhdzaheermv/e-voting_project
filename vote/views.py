from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Voter
from django.contrib.auth.hashers import make_password  # To hash passwords
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password

def index(request):
    return render(request, 'index.html')

def voter_registration(request):
    if request.method == 'POST':
        # Get form data
        fullname = request.POST.get('fullname')
        username = request.POST.get('username')
        phonenumber = request.POST.get('phonenumber')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_picture = request.FILES.get('profile_picture')  # Get the uploaded file

        # Hash the password for security
        hashed_password = make_password(password)

        # Create a new voter with the uploaded profile picture
        Voter.objects.create(
            fullname=fullname,
            username=username,
            phonenumber=phonenumber,
            email=email,
            password=hashed_password,
            profile_picture=profile_picture  # Save the profile picture
        )

        return HttpResponse("Registration successful! Please login.")
    
    return render(request, 'voter_registration.html')

def voter_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            voter = Voter.objects.get(username=username)
            if check_password(password, voter.password):  # Check if the password matches
                # After successful login, render the voter home page
                return render(request, 'voter_home.html', {'voter': voter})
            else:
                return HttpResponse("Invalid username or password.")
        except Voter.DoesNotExist:
            return HttpResponse("Invalid username or password.")
    
    return render(request, 'voter_login.html')

def voter_logout(request):
    logout(request)
    return redirect('vote:index') 
