from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('about', views.about),
    path('map', views.map),
    path('news',views.news),
    path('search',views.search, name = 'search'),
    path('important', views.important)
]