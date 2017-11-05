from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from firebase import firebase
from time import time
from datetime import datetime, timedelta

import json
import subprocess
import random

my_firebase = firebase.FirebaseApplication('https://test-cdf02.firebaseio.com', None)

@csrf_exempt
@require_http_methods(["POST"])
def post1(requst):
    return HttpResponse("ok")

@csrf_exempt
@require_http_methods(["POST"])
def rateDay(request):
    username = request.POST["username"]
    mood = int(request.POST["mood"])
    print(username, mood)
    obj = {int(time()*1000): mood}
    result = my_firebase.patch('https://test-cdf02.firebaseio.com/mood_events/'+username, obj)
    print(result)
    return HttpResponse("ok")

def getUsers(request):
    users = my_firebase.get("/users", None)
    return HttpResponse(json.dumps(users))

def getProjects(request):
    projects = my_firebase.get("/projects", None)
    return HttpResponse(json.dumps(projects))


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
    commits = json_data["commits"]
  
    for commit in commits:
        added = 0
        modified = 0
        removed = 0
        try:
            added += len(commit["added"])
        except:
            pass
        try:
            modified += len(commit["modified"])
        except:
            pass
        try:
            removed += len(commit["removed"])
        except:
            pass
        github_username = commit["committer"]["username"]

        utc_time = datetime.strptime("2017-09-15T17:13:29.380Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        #milliseconds = (utc_time - datetime(1970, 1, 1)) // timedelta(milliseconds=1)
        milliseconds = int((utc_time - datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)
        # print(milliseconds)

        # year = commit["timestamp"][0:4]
        # month = commit["timestamp"][5:7]
        # day = commit["timestamp"][8:10]
        # hour = commit["timestamp"][11:13]
        # minute = commit["timestamp"][14:16]
        # second = commit["timestamp"][17:19]
        # print(added,modified,removed)
        # print(year, month, day)
        # print(hour, minute, second)
        obj = {
            milliseconds: {
                "code_quality": random.random(),    #TO DO
                "files_added": added,
                "files_changed": modified,
                "files_removed": removed
            }
        }

        result = my_firebase.patch('https://test-cdf02.firebaseio.com/git_events/' + github_username, obj)

    return HttpResponse(result)

def getAverageEventsWeekly(request):
    today = int(time() * 1000) // (1000 * 60 * 60 * 24)
    
    #event_types = ["humidity_events", "temperature_events", "light_events", "motion_events", "noise_events"]
    duck_events = my_firebase.get("/duck_events_mock", None)
    out = {}
    for duck_event_type in duck_events:
        out[duck_event_type] = [0, 0, 0, 0, 0, 0, 0]
        sumEvents = [0, 0, 0, 0, 0, 0, 0]
        cntEvents = [0, 0 ,0 ,0 ,0, 0, 0]
        for duck_id in duck_events[duck_event_type]:
            for event_timestamp in duck_events[duck_event_type][duck_id]:
                value = int(duck_events[duck_event_type][duck_id][event_timestamp])
                day = int(event_timestamp) // (1000 * 60 * 60 * 24)
                daysAgo = today - day
                if (daysAgo < 7):
                    sumEvents[daysAgo] += value
                    cntEvents[daysAgo] += 1
        for i in range(7):
            if cntEvents[i] > 0:
                out[duck_event_type][i] = sumEvents[i] // cntEvents[i]
            else:
                out[duck_event_type][i] = -1
        out[duck_event_type].reverse()
    return HttpResponse(json.dumps(out))

def getAverageMoodsWeekly(request):
    today = int(time() * 1000) // (1000 * 60 * 60 * 24)
    averageMoods = [None, None, None, None, None, None, None]
    sumMoods = [0, 0, 0, 0, 0, 0, 0]
    cntMoods = [0, 0, 0, 0, 0, 0, 0]
    mood_events = my_firebase.get("/mood_events_mock", None)
    for user_id in mood_events:
        print(user_id)
        for timestamp in mood_events[user_id]:
            value = int(mood_events[user_id][timestamp])
            print(value)
            day = int(timestamp) // (1000 * 60 * 60 * 24)
            daysAgo = today - day
            print("d",daysAgo)
            if (daysAgo < 7):
                sumMoods[daysAgo] += value
                cntMoods[daysAgo] += 1

    for i in range(7):
        if cntMoods[i] > 0:
            averageMoods[i] = sumMoods[i] // cntMoods[i]
        else:
            averageMoods[i] = 0

    print(averageMoods)
    averageMoods.reverse()
    print(averageMoods)
    return HttpResponse(json.dumps(averageMoods))


def getLists(request):
    ducks = my_firebase.get("/ducks", None)
    return HttpResponse(json.dumps(ducks))

def getTimestamp(request):
    return HttpResponse(int(time()*1000))

def createModelData():
    
    my_firebase = firebase.FirebaseApplication('https://test-cdf02.firebaseio.com', None)
    users = my_firebase.get("/users", None)
    # print(users)
    # print("*************")
    mood_events = my_firebase.get("/mood_events_mock", None)
    duck_events = my_firebase.get("/duck_events_mock", None)

    model={}
    for user_id in users:
        model[user_id] = {}
        # print("--------")
        # print(user_id)
        duck_id = users[user_id]['duck_id']
        # print("duck_id: ", duck_id)
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
                # print("day ", day)


                event_types = ["noise_events", "temperature_events"]

                for event_type in event_types:  
                    suma = 0
                    cnt = 0
                    try:
                        type_events = duck_events[event_type][duck_id]
                        # print("type_events")
                        # print(type_events)
                        for type_event_timestamp in type_events:
                            type_event_day = int(type_event_timestamp) / (1000 * 60 * 24)
                            # print('type_day', type_event_day)
                            if (day == type_event_day):
                                # print("isti:::::::::::::::::::::::")
                                suma += int(type_events[type_event_timestamp])
                                cnt += 1
                    except:
                        pass
                    # print("**1")
                    if (cnt > 1):
                        user_type_avg = float(suma)/cnt
                        model[user_id][day][event_type] = user_type_avg
                    # print("**2")

        except:
            pass
        #print(user_id)
        #print(user_mood_events)
    # print()
    # print()
    # print(model)


if __name__ == "__main__":	
    createModelData()
