from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'gastro_app/login.html')

def index(request):
    return render(request, 'gastro_app/index.html')