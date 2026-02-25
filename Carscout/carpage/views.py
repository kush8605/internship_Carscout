from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url= 'login')
def home(request):
    return render(request, 'carpage/home.html')

@login_required(login_url= 'login')
def adminhome(request):
    return render(request, 'carpage/adminhome.html')

