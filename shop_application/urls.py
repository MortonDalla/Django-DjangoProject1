from django.conf.urls import url
from.views import user_registrations

urlpatterns = [
    url(r'^add/shop_application/$', user_registrations, name='user_registrations'),
]