from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pet

@login_required(login_url='/login/')
def list_all_pets(request):
    pet = Pet.objects.filter(active=True)
    context = {
        'pet': pet
    }
    return render(request, 'list.html', context)   

def list_user_pets(request):
   pet = Pet.objects.filter(active=True, user=request.user) 
   context = {
       'pet': pet
   }   
   return render(request, 'list.html', context)   

def pets_detail(request, id):
    pet = Pet.objects.get(id=id)
    context = {
        'pet': pet
    }
    return render(request, 'pet.html', context)   



def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/login/')    

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')    
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou senha inválidos. Por favor tente novamente.')
            return redirect('/login/')            
        
            