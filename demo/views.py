from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib.auth import logout as django_logout


@login_required
def index(request):
    """Index view"""
    try:
        social = SocialAccount.objects.get(user=request.user)
        context = {
            "name": social.user.get_full_name(),
            "avatar": social.get_avatar_url()
        }
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        context = None
    return render(request, 'demo/index.html', context)


def login(request):
    """Login view"""
    return render(request, 'demo/login.html')


def logout(request):
    """Logout view"""
    django_logout(request)
    return HttpResponseRedirect(reverse_lazy('demo:index'))


def de_authorize(request):
    """Facebook De-authorize callback view"""
    return render(request, 'demo/de-auth.html')
