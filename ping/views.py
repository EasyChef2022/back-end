from django.http import HttpResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def ping(request):
    return HttpResponse("pong")