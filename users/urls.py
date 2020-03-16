from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('signup.html/', views.signup, name='signup'),
    path('login.html/', views.login, name='login'),
    path('login\.html/login.html', views.login, name='login'),
    path('info.html/', views.info, name='info'),   
    path('registration.html/<email>/', views.registration, name='registration'),
    path('signup.html/POST', views.registration, name='registration'),
    path('signup.html/search.html', views.search, name='search'),
    path('signup.html/partial.html', views.partial, name='partial'),
    url(r'^signup.html/signup.html/partial.html/(?P<car_plate>[-\w]+)/$', views.partialDetail, name='partialSearch'),
   
    path('login.html/<email>/', views.profile, name='profile'),

]