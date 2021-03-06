from django.conf.urls import url 
from crudapi import views 
from django.urls import path, include
app_name = 'crudapi'
urlpatterns = [
    url(r'^api/companies/$', views.company_list),
    url(r'^api/companies/([0-9]+)$', views.company_detail),
    path('create/', views.create_session),
    path('access/', views.access_session),
    path('delete/', views.delete_session),
    path('subscribe/', views.subscribe, name = 'subscribe'),
    path('register/', views.registerUser.as_view(), name='registerUser'),
    path('login/', views.loginUser.as_view(), name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
]
