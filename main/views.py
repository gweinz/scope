from django.shortcuts import render, redirect

# Create your views here.

def main(response):
    
    return render(response, 'main/main.html')