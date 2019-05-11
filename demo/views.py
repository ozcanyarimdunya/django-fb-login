from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy


def index(request):
    """Index view"""
    ctx = {
        "name": "Ozcan Yarimdunya",
        "avatar": "https://avatars0.githubusercontent.com/u/12237463?s=460&v=4"
    }
    return render(request, 'demo/index.html', context=ctx)


def login(request):
    """Login view"""
    return render(request, 'demo/login.html')


def logout(request):
    """Logout view"""
    ctx = {
        "message": "Thanks for spending time on website."
    }
    return HttpResponseRedirect(reverse_lazy('demo:index'))


def de_authorize(request):
    """Facebook De-authorize callback view"""
    return render(request, 'demo/de-auth.html')
