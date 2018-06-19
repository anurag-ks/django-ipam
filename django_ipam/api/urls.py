from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^subnet/(?P<subnet_id>[0-9a-f-]+)/iprequest/$', views.iprequest, name='iprequest'),
]
