from django.shortcuts import render, redirect
from .forms import UserForm, StudentForm
from .models import Student
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


def register_user(request):

    userform = UserForm()
    studentform = StudentForm()

    context = {
        'userform': userform,
        'studentform': studentform
    }

    if request.method == 'POST':
        userform = UserForm(request.POST)
        studentform = StudentForm(request.POST)

        if userform.is_valid() and studentform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()

            user_info = studentform.save(commit=False)
            user_info.user = user
            user_info.save()

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            login(request, user)
            return redirect('home')

        else:
            context = {'userform': userform,
                       'studentform': studentform, 'user_form.errors': userform.errors,
                       'user_info_form.errors': studentform.errors}
            return render(request, 'register.html', context)

    return render(request, 'register.html', context=context)


def login_user(request):

    context = {
        'check': False
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        else:
            context = {
                'check': True
            }

    return render(request, 'login.html', context)


@login_required(login_url='error')
def home(request):
    return render(request, 'home.html')


def error(request):
    return render(request, 'error.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('index')
