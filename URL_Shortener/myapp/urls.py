from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('hello',views.hello_world),
    path('',views.home_page),
    path('all-analytics',views.all_analytics),
    path('analytics/<slug:shorturl>',views.single_analytics),
    path('<slug:shorturl>',views.redirect_url)
]