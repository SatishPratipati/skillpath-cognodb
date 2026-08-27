from django.urls import path
from explorer import views

urlpatterns = [
    path("", views.home, name="home"),
    path("explore/", views.explore, name="explore"),
    path("path/", views.career_path, name="career_path"),
]
