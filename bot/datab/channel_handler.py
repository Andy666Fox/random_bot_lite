import json 
import random 


def get_random_channel():
    with open('words.json', 'r') as file:
        data = json.load(file)

    return [random.choice(list(data.keys())) for _ in range(100)]
