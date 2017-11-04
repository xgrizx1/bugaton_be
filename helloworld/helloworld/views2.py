from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from firebase import firebase
from time import time


import json
import subprocess

my_firebase = firebase.FirebaseApplication('https://test-cdf02.firebaseio.com', None)


@csrf_exempt
@require_http_methods(["GET"])
def recodEvent(request):
    duckId = request.GET["duck"]
    eventType = request.GET["event"]
    eventValue = request.GET["value"]
    timestamp = int(time() * 1000)
    my_firebase.patch("https://test-cdf02.firebaseio.com/duck_events/"+eventType+"/"+duckId,{timestamp: eventValue})
    return HttpResponse("ok")
