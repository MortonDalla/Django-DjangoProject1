"""
Definition of urls for python_webapp_django.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import shop_application.forms
import shop_application.views
import shop_application.urls

from django.conf.urls import url, include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', shop_application.views.home, name='home'),
    url(r'^', include('shop_application.urls')),
    url(r'^contact$', shop_application.views.contact, name='contact'),
    url(r'^about', shop_application.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': shop_application.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
