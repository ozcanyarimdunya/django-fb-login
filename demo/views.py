import traceback

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib.auth import logout as django_logout
from django.views.decorators.csrf import csrf_exempt

from demo.utils import FacebookUserIdDecoder


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


@csrf_exempt
def de_authorize(request):
    try:
        decoder = FacebookUserIdDecoder(request_data=request.POST)
        user_id = decoder.get_user_id()
    except:
        traceback.print_exc()
        return HttpResponse(status=400, content='Cannot decode request')

    try:
        user = SocialAccount.objects.get(uid=user_id).user
        user.is_active = False
        user.save()
    except(ObjectDoesNotExist, MultipleObjectsReturned):
        traceback.print_exc()
        return HttpResponse(status=400, content='User not found')
    return HttpResponse(status=200)
