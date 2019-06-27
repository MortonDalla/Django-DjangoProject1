"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from.forms import BootstrapAuthenticationForm
import shop_application.models
# from django_proct1_shoppig.shop_application.models import RegisterUsers

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

def login(request):
    queryset = shop_application.models.objects.all()
    assert isinstance(request, HttpRequest)



    return render(
        request,
        'app/login.html',
        {
            'title':'Contact',
            'context':queryset,
            'year':datetime.now().year,
        }
    )


    # queryset = BootstrapAuthenticationForm.objects.all()
    # if request.method == "POST":
    #     form = BootstrapAuthenticationForm(request.POST)
    # context = {
    # 'posts': BootstrapAuthenticationForm.objects.all()
    # }
    #
    # return render(request, "app/login.html", context)