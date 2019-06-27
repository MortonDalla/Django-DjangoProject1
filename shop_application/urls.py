from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView
from.views import user_registrations

urlpatterns = [
    url(r'^add/shop_application/$', user_registrations, name='user_registrations'),
    path('login/', LoginView.as_view(), name="login_url"),
    path('register/', user_registrations, name="register_url"),

]