from . import views
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('register/', views.UserCreate),
    path('login/', views.UserLogin),
    path('logout/', views.logout_view),
    path('profile/', views.Profile),
    path('image/', views.UploadImage),
    path('allImages/', views.AllImages),
]