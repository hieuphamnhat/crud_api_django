from django.conf.urls import url 
from crudapi import views 
from django.urls import path

urlpatterns = [
    url(r'^api/companies/$', views.company_list),
    url(r'^api/companies/(?P<pk>[0-9]+)$', views.company_detail),
    path('create/', views.create_session),
    path('access/', views.access_session),
    path('delete/', views.delete_session),
    path('subscribe/', views.subscribe, name = 'subscribe'),
]
