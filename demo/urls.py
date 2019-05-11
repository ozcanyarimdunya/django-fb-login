from django.urls import path

from demo import views

app_name = 'demo'
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("de-auth/", views.de_authorize, name="de-auth"),
]
