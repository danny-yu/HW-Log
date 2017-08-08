from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .models import Course
from .forms import ClassEnrollForm


def home(request):
    course_list = Course.objects.all()
    context = {
        'course_list':course_list,
    }
    return render(request,'log/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def configure(request):
    if request.method == 'POST':
        form = ClassEnrollForm(request.POST)
        if form.is_valid():
            course_1 = form.cleaned_data['course_1']
            course_1.students.add(request.user)
            return redirect('home')
    else:
        form = ClassEnrollForm()
    return render(request, 'configure.html', {'form': form})
