"""
Definition of views.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from .forms import RegisterUsersForm, BootstrapAuthenticationForm
from.models import RegisterUsers
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

from django import forms

# @login_required
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Small Businesses Online Shopping Centre(coming soon).',
            'year':datetime.now().year,
        }
    )

def shop(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/shop.html',
        {
            'title':'shop',
            'message':'Small Businesses Online Shopping Centre(coming soon).',
            'year':datetime.now().year,
        }
    )

def product(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/product-details.html',
        {
            'title':'products',
            'message':'Small Businesses Online Shopping Centre(coming soon).',
            'year':datetime.now().year,
        }
    )

def cart(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/cart.html',
        {
            'title':'cart',
            'message':'Small Businesses Online Shopping Centre(coming soon).',
            'year':datetime.now().year,
        }
    )

def checkout(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/checkout.html',
        {
            'title':'checkout',
            'message':'Small Businesses Online Shopping Centre(coming soon)..',
            'year':datetime.now().year,
        }
    )

def loginView(request):
    return render(request, "registration/register.html")

def user_registrations(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('login_url')
    else:
        form = UserCreationForm
    return render(request, "registration/register.html", {'form':form})
