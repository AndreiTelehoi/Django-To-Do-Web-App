from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm

# Create your views here.


def home(req):
    return render(req, 'todo/home.html')


def signup_user(req):
    if req.method == "GET":
        return render(req, 'todo/signup_user.html', {'form': UserCreationForm()})
    else:
        if req.POST['password1'] == req.POST['password2']:
            try:
                user = User.objects.create_user(
                    req.POST['username'], password=req.POST['password1'])
                user.save()
                login(req, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(req, 'todo/signup_user.html', {
                    'form': UserCreationForm(),
                    'error': 'username already taken'
                })
        else:
            return render(req, 'todo/signup_user.html', {
                'form': UserCreationForm(),
                'error': 'Passwords did not match'
            })


def login_user(req):
    if req.method == "GET":
        return render(req, 'todo/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            req, username=req.POST['username'], password=req.POST['password'])
        if user is None:
            return render(req, 'todo/login_user.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(req, user)
            return redirect('current_todos')


def logout_user(req):
    if req.method == 'POST':
        logout(req)
        return redirect('home')


def create_todo(req):
    if req.method == 'GET':
        return render(req, 'todo/create_todo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(req.POST)
            new_todo = form.save(commit=False)
            new_todo.user = req.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            return render(req, 'todo/create_todo.html', {'error': 'Bad data'})


def current_todos(req):
    return render(req, 'todo/current_todos.html')
