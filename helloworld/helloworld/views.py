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

    model={}
    for user_id in users:
        model[user_id] = {}
        print("--------")
        print(user_id)
        duck_id = users[user_id]['duck_id']
        print("duck_id: ", duck_id)
        user_mood_events = None

        sume = []
        cnts = []
        avgs = []

        try:
            #all user mood events
            user_mood_events = mood_events[user_id]
            print(user_mood_events)
            #all days
            for timestamp in user_mood_events:
                day = int(timestamp) / (1000 * 60 * 24)
                model[user_id][day] = {}
                print("day ", day)


                event_types = ["noise_events", "temperature_events"]

                for event_type in event_types:  
                    suma = 0
                    cnt = 0
                    try:
                        type_events = duck_events[event_type][duck_id]
                        print("type_events")
                        print(type_events)
                        for type_event_timestamp in type_events:
                            type_event_day = int(type_event_timestamp) / (1000 * 60 * 24)
                            print('type_day', type_event_day)
                            if (day == type_event_day):
                                suma += int(type_events[type_event_timestamp])
                                cnt += 1
                    except:
                        pass
                    print("**1")
                    if (cnt > 1):
                        user_type_avg = float(suma)/cnt
                        model[user_id][day][event_type] = user_type_avg
                    print("**2")



                """
                suma = 0
                cnt = 0

                #noise events avg for user
                try:
                    noise_events = duck_events["noise_events"][duck_id]
                    print("noise_events")
                    print(noise_events)
                    for noise_event_timestamp in noise_events:
                        noise_event_day = int(noise_event_timestamp) / (1000 * 60 * 24)
                        print('noise_day', noise_event_day)
                        if (day == noise_event_day):
                            suma += int(noise_events[noise_event_timestamp])
                            cnt += 1
                except:
                    pass
                print("**1")
                user_noise_avg = float(suma)/cnt
                model[user_id][day]["noise"] = user_noise_avg
                print("**2")

                suma = 0
                cnt = 0
                #temperature events avg for user
                try:
                    temperature_events = duck_events["temperature_events"][duck_id]
                    print("noise_events")
                    print(temperature_events)
                    for temperature_event_timestamp in temperature_events:
                        temperature_event_day = int(temperature_event_timestamp) / (1000 * 60 * 24)
                        print('temperature_event_day', temperature_event_day)
                        if (day == temperature_event_day):
                            suma += int(temperature_events[temperature_event_timestamp])
                            cnt += 1
                except:
                    pass
                print("**1")
                user_noise_avg = float(suma)/cnt
                model[user_id][day]["noise"] = user_noise_avg
                print("**2")
                """
        except:
            pass
        #print(user_id)
        #print(user_mood_events)
    print(model)


if __name__ == "__main__":	
    createModelData()