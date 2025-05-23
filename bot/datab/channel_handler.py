import json 
import random 


def get_random_channel():
    with open('bot\\datab\\val_channels.json', 'r') as file:
        data = json.load(file)

    return random.choice(list(data.keys()))
