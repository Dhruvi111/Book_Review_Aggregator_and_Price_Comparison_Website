from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Home"),
    path('about/', views.about, name="About"),
    path('contact/', views.contact, name="Contact"),
    path('search/', views.search, name="Search"),
    path('genre/<str:category>/', views.genre, name="Genre"),
    path('login/', views.login, name="Login"),
    path('signup/', views.signup, name="Signup"),
    path('details/', views.details, name="Details"),
    path('detailsHome/', views.detailsHome, name="DetailsHome"),
    path('page/<int:digit>', views.pages, name="page")
]
