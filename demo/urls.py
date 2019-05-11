from django.urls import path

from . import views

app_name = 'demo'
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("de-auth/", views.de_authorize, name="de-auth"),
]
