from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Home"),
    path('about/', views.about, name="About"),
    path('contact/', views.contact, name="Contact"),
    path('search/', views.search, name="Search"),
    path('genre/<str:category>/', views.genre, name="Genre"),
    path('signin/', views.signin, name="SignIn"),
    path('signup/', views.signup, name="Signup"),
    path('signout/', views.signout, name="Signout"),
    path('details/', views.details, name="Details"),
    path('detailsHome/', views.detailsHome, name="DetailsHome"),
    path('page/<int:digit>', views.pages, name="page"),
    path('reviewBNoble/', views.BNoble, name="BNoble"),
    path('reviewBookmarks/', views.Bookmarks, name="Bookmarks"),
    path('reviewAmazon/', views.Amazon, name="Amazon"),
    path('reviewGoodreads/', views.Goodreads, name="Goodreads"),
    path('userProfile/', views.favourites, name="Favourites"),
    path('userProfile/d', views.favDelete, name="FavDelete"),
    # path('reviewLibraryThing/', views.LibraryThing, name="LibraryThing"), 
    
]
