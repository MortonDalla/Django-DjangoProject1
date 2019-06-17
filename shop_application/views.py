"""
Definition of views.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import RegisterUsersForm, BootstrapAuthenticationForm
from.models import RegisterUsers
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from django import forms

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


def user_registrations(request):
    if request.method == "POST":
        form = RegisterUsersForm(request.POST)
        if form.is_valid():
            add_shop_application_item = form.save(commit=False) #commit - the data has never been stored in the DB
            add_shop_application_item.save()

            userobj = form.cleaned_data

            first_name = userobj['first_name']
            last_name = userobj['last_name']
            user_name = userobj['user_name']
            password = userobj['password']
            email_address = userobj['email_address']
            description = userobj['description']
            contact_numbers = userobj['contact_numbers']

            if not (RegisterUsers.objects.filter(user_name=user_name).exists() or RegisterUsers.objects.filter(email_address=email_address).exists()):
                RegisterUsers.objects.create_user(user_name, email_address, password)
                user = BootstrapAuthenticationForm(user_name=user_name, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form = RegisterUsersForm
                #raise forms.ValidationError('Looks like a username with that email or password already exists')

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
            form = RegisterUsersForm
    else:
        form = RegisterUsersForm
    return render(request, "shop_application/register_users.html", {'form': form})


# def user_registrations(request):
#     queryset = RegisterUsers.objects.all()
#     if request.method == "POST":
#         form = BootstrapAuthenticationForm(request.POST)
#     context = {
#     'posts': RegisterUsers.objects.all()
#     }
#
#     return render(request, "app/login.html", context)
#     # if request.method == "POST":
#     #     form = BootstrapAuthenticationForm(request.POST)
#     #     if form.is_valid():
#     #         add_shop_application_item = form.save(commit=False)
#     #         add_shop_application_item.save()
#     #         form = RegisterUsersForm
#     # else:
#     #     form = RegisterUsersForm
#     #return render(request, "app/index.html", {'form': form})
