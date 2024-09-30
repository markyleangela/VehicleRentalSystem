
from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

def index(request):
    if request.method == 'POST':
        return redirect('login_page')
    return render(request, 'landing_page.html')

