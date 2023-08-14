from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('main:index')
        else:
            messages.success(request, ("There was an error logging in"))
            return redirect('login:login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('main:index')


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect("main:index")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {
        'form': form,
    })
