from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pet

@login_required(login_url='/login/')
def register_pet(request):
    pet_id = request.GET.get('id');

    if pet_id:
        pet = Pet.objects.get(id=pet_id)

        if pet.user == request.user:
            return render(request, 'register-pet.html', {'pet': pet})
    return render(request, 'register-pet.html')

@login_required(login_url='/login/')
def set_pet(request):

    city = request.POST.get('city')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    description = request.POST.get('description')
    photo = request.FILES.get('file')
    pet_id= request.POST.get('pet-id')
    user = request.user
    
    if pet_id:
        pet = Pet.objects.get(id=pet_id)

        if user == pet.user:
            pet.email = email
            pet.phone = phone
            pet.city = city
            pet.description = description

            if photo:
                pet.photo = photo

            pet.save()
    else:        
        pet = Pet.objects.create(
            city = city,
            email=email,
            phone=phone,
            description=description,
            photo=file,
            user=user 
        ) 
    url = '/pet/detail/{}/'.format(pet.id)
    return redirect(url)

@login_required(login_url='/login/')
def delete_pet(request, id):
    pet = Pet.objects.get(id=id)
    
    if pet.user == request.user:
        pet.delete()
        
    return redirect('/')

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
        
            