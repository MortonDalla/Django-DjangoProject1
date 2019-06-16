"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import RegisterUsersForm

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
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def user_registrations(request):
    if request.method == "POST":
        form = RegisterUsersForm(request.POST)
        if form.is_valid():
            add_shop_application_item = form.save(commit=False) #commit - the data has never been stored in the DB
            add_shop_application_item.save()
            form = RegisterUsersForm
    else:
        form = RegisterUsersForm
    return render(request, "shop_application/register_users.html", {'form': form})