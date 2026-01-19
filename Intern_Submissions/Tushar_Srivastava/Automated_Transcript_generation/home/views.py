from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse

def home_view(request):
    context = {'page':'home'}
    return render(request, 'index.html',context)

def login_view(request):
    context = {'page':'login'}
    return render(request, 'login.html', context)
def signup_view(request):
    context = {'page':'signup'}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after signup
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home') 
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html',{'form': form})