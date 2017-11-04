from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from firebase import firebase
from time import time

import json
import subprocess

my_firebase = firebase.FirebaseApplication('https://test-cdf02.firebaseio.com', None)

def index(request):
    #f = open("test2.txt","w")
    output = subprocess.check_output("echo 1+2", shell=True)
    #subprocess.call("./test.sh", shell=True)
    #subprocess.call("bash & ls", shell=True)
    #subprocess.call("ls", shell=True)
    #subprocess.call("echo zdava", shell=True)
    return HttpResponse(output)

def gitClone(request):
    subprocess.call("git clone https://github.com/xgrizx1/bugaton_fe/", shell=True)
    subprocess.call("git --git-dir=./bugaton_fe/.git pull --all")
    output = subprocess.check_output("git --git-dir=./bugaton_fe/.git diff --shortstat dbb5281ef6ea26e85c34bcff8271ee5702be03a8 31d133d3dd9a39d42a654958ff77b9c99be81cb6")
    #subprocess.call("cd bugaton_fe & git pull --all", shell=True)
    #output = subprocess.check_output("cd bugaton_fe & ls", shell=True)
    #subprocess.call("cd bugaton_fe", shell=True)
    #output += subprocess.check_output("cd bugaton_fe & git diff --shortstat dbb5281ef6ea26e85c34bcff8271ee5702be03a8 31d133d3dd9a39d42a654958ff77b9c99be81cb6", shell=True)
    return HttpResponse(output)

def ls(request):
    output = subprocess.check_output("ls", shell=True)
    return HttpResponse(output)

@csrf_exempt
@require_http_methods(["POST"])
def hooks(request):
    
    json_data = json.loads(request.POST["payload"])
    result = my_firebase.patch('https://test-cdf02.firebaseio.com/test_push2', json_data)
    
    return HttpResponse(result)

def getLists(request):
    ducks = my_firebase.get("/ducks", None)
    return HttpResponse(json.dumps(ducks))

def getTimestamp(request):
    return HttpResponse(int(time()*1000))

def createModelData():
    
    my_firebase = firebase.FirebaseApplication('https://test-cdf02.firebaseio.com', None)
    users = my_firebase.get("/users", None)
    print(users)
    print("*************")
    mood_events = my_firebase.get("/mood_events", None)
    duck_events = my_firebase.get("/duck_events", None)
    for user_id in users:
        duck_id = users[user_id]['duck_id']
        user_mood_events = None
        try:
            #all user mood events
            user_mood_events = mood_events[user_id]
            #all days
            for timestamp in user_mood_events:
                day = timestamp / (1000 * 60 * 24)
                suma[day] = 0
                cnt[day] = 0
                #noise events for 
                try:
                    noise_events = duck_events["noise_events"][duck_id]
                    for noise_event_timestamp in noise_events:
                        noise_event_day = noise_event_timestamp / (1000 * 60 * 24)
                        if (day == noise_event_day):
                            suma[day] += noise_events[noise_event_timestamp]
                            cnt[day] += 1

                except:
                    pass
                print(timestamp)
        except:
            pass
        print(user_id)
        print(user_mood_events)
        #print duck_id


if __name__ == "__main__":	
    createModelData()