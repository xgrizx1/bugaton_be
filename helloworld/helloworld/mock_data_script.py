from firebase import firebase
from time import time
import random

if __name__ == "__main__":	
    event_types = ["humidity_events", "temperature_events", "light_events", "motion_events", "noise_events"]
    emotion_list = [1, 2, 3, 4, 5]

    now = int(time() * 1000)

    days_timestamps = []

    duck_id = "duck1"
    name = "jack"

    for i in range(30):
        days_timestamps.append(now - (30-i) * 24 * 60 * 60 * 1000)

    emotions_events = {}
    duck_events = {}
    for event_type in event_types:
        duck_events[event_type] = {}
        duck_events[event_type][duck_id] = {}
    emotions_events[name] = {}
    for i in range(30):
        #print(i, " ", days_timestamps[i])
        emotion = random.choice(emotion_list)
        emotions_events[name][days_timestamps[i]] = emotion
        value = {}
        #temperature
        value['temperature_events'] = 25 + random.choice([1, -1]) * random.randint(0, (6 - emotion) * 2)
        #motion
        if (random.random() > 0.2 * (6 - emotion)):
            value['motion_events'] = 0
        else:
            value['motion_events'] = 255
        #noise
        value['noise_events'] = 50 + int((6 - emotion) * 40 * random.random())
        #light
        value['light_events'] = 137 + int(random.random() * random.choice([1, -1]) * (6 - emotion) * 5)
        #humidity
        value['humidity_events'] = 35 + int(random.random() * random.choice([1, -1]) * (6 - emotion) * 3)

        for event_type in event_types:
            duck_events[event_type][duck_id][days_timestamps[i]] = value[event_type]

    # print(emotions_events)
    # print("---------------------------------")
    # print(duck_events)

    my_firebase = firebase.FirebaseApplication('https://test-cdf02.firebaseio.com', None)
    result = my_firebase.patch('https://test-cdf02.firebaseio.com/mood_events_mock', emotions_events)
    result = my_firebase.patch('https://test-cdf02.firebaseio.com/duck_events_mock', duck_events)
    print(result)