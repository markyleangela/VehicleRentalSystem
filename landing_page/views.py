
from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

def index(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'login':
            return redirect('login_page')
        elif request.POST.get('action') == 'register':
            return redirect('register')
    return render(request, 'landing_page.html')

