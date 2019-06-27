"""
Definition of urls for python_webapp_django.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.contrib.auth.views import LoginView
import app.views
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
    url(r'^shop', shop_application.views.shop, name='shop'),
    url(r'^products', shop_application.views.product, name='products'),
    url(r'^cart', shop_application.views.product, name='cart'),
    url(r'^checkout', shop_application.views.checkout, name='checkout'),
    url(r'^register', shop_application.views.user_registrations, name='register'),
    url(r'^login', LoginView.as_view(), name="login"),
    # url(r'^login/$', LoginView.as_view(template_name='app/login.html'),
    #     name='restaurant-sign-in'),
    # url(r'^login/$',
    #     LoginView.as_view,
    #     {
    #         'template_name': 'app/login.html',
    #         'authentication_form': shop_application.forms.BootstrapAuthenticationForm,
    #         'extra_context':
    #             {
    #                 'title': 'Log in',
    #                 'year': datetime.now().year,
    #             }
    #     },
    #     name='login'),

    url(r'^logout$',
        django.contrib.auth.views.LogoutView,
        {
            'next_page': '/',
        },
        name='logout'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
]


