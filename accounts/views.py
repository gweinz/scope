from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
import bets.views

def register(response):
    if response.method == "POST":
        form = UserForm(response.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(response, f'Account created for {username}!')
            user = form.save()
            

        #go to homepage
        redirect("/main")
    else:
        form = UserForm()
       
    return render(response, "accounts/register.html", {"form":form})

