from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from firebase import firebase

import json

def index(request):
    return HttpResponse("hhelo")

@csrf_exempt
@require_http_methods(["POST"])
def hooks(request):
    json_data = json.loads(request.body)
    my_firebase = firebase.FirebaseApplication('https://test-cdf02.firebaseio.com', None)
    result = my_firebase.patch('https://test-cdf02.firebaseio.com/test_push2', json_data)
    
    return HttpResponse(result)