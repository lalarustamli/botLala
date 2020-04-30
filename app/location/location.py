import math
import datetime
import json
import operator
import numpy as np
from app import chatbot


def calculate_haversine(user_coordinates, branch_coordinates):
    """Return the great-circle distance between two points by the 'haversine' formula.
    Source: http://www.movable-type.co.uk/scripts/latlong.html
    Source: https://stackoverflow.com/a/21623256
    """
    R = 6371
    user_lat, user_long = user_coordinates
    branch_lat, branch_long = branch_coordinates

    a = 0.5 - math.cos((branch_lat - user_lat) * math.pi / 180) / 2 + \
        math.cos(user_lat * math.pi / 180) * math.cos(branch_lat * math.pi / 180) * \
        (0.5 - math.cos((branch_long - user_long) * math.pi / 180) / 2)

    return R * 2 * math.asin(math.sqrt(a))


def get_nearest_atm(user_coordinates):
    """Return the nearest ATM object by comparing <user_coordinates> 
    with ATM coordinates.
    """
    with open("files/branches.json", encoding="utf-8") as branches_json:
        branches = json.load(branches_json)

    branch_to_distance = {}

    for branch in branches:
        branch_coordinates = tuple(
            (float(coordinates) for coordinates in branch['coordinates'].split(',')))
        # each branch mapped to the distance between user's location
        branch_to_distance[branch['ATM']] = calculate_haversine(
            user_coordinates, branch_coordinates)

    # sort branch_to_distance dictionary according to values (distances between user's location)
    branches_sorted_by_distance = sorted(
        branch_to_distance.items(), key=operator.itemgetter(1))

    nearest_branch_id = branches_sorted_by_distance[0][0]
    nearest_branch = {}

    for branch in branches:
        if branch['ATM'] == nearest_branch_id:
            nearest_branch = branch

    return nearest_branch


def get_message_with_map(nearest_branch):
    '''Return the location of the nearest ATM on map object to user.
    '''

    # create map object for facebook with yandex map image
    branch_coordinates = nearest_branch['coordinates'].split(',')
    image_url = "https://static-maps.yandex.ru/1.x/?lang=tr_TR&ll=" + \
                branch_coordinates[1] + "," + branch_coordinates[0] + \
                "&size=545,280&z=16&l=map&pt=" + branch_coordinates[1] + \
                "," + branch_coordinates[0] + ",round"
    item_url = "http://maps.apple.com/maps?q=" + \
               branch_coordinates[0] + "," + branch_coordinates[1] + "&z=16"

    message = {
        'attachment': {
            'type': 'template',
            'payload': {
                'template_type': 'generic',
                'elements': {
                    'element': {
                        'title': nearest_branch['name'],
                        'subtitle': nearest_branch['address'],
                        'image_url': image_url,
                        'item_url': item_url
                    }
                }
            }
        }
    }
    return message


def ask_location_from_user(sender_id, step=0):
    """Return facebook quick_replies message to ask user's current location from map.
    """
    text = ""
    quick_reply = []

    if step == 0:
        text = 'Xahiş edirik hal-hazırkı yerinizi bizimlə paylaşın.'
        quick_reply = [{'content_type': 'location'}]

        sender = {'sender_id': sender_id,
                  'step': 0,
                  'state': chatbot.LOCATION_STATE[1],
                  'status': chatbot.STATE_STATUS[0],
                  'start_timestamp': datetime.datetime.now(),
                  'user_data': {}}
        chatbot.insert_sender(sender)
    else:
        new_values = {'$set': {}}
        sender = chatbot.find_sender(sender_id, chatbot.LOCATION_STATE[1])
        new_values['$set']['status'] = chatbot.STATE_STATUS[2]
        chatbot.update_sender(sender, new_values)
        user_coordinates = (sender['user_data']['lat'], sender['user_data']['long'])
        return get_message_with_map(get_nearest_atm(user_coordinates))

    message = {
        'text': 'Xahiş edirik hal-hazırkı yerinizi bizimlə paylaşın.',
        'quick_replies': [{'content_type': 'location'}]
    }
    return message


def save_location_from_user(sender, user_message):
    print(str(sender))
    step = sender['step']
    new_values = {'$set': {}}

    if step == 0:
        if (user_message.get('attachments') and
                user_message['attachments'][0]['type'] == "location"):
                user_coordinates = (user_message['attachments'][0]['payload']['coordinates']['lat'],
                                    user_message['attachments'][0]['payload']['coordinates']['long'])

                nearest_atm = get_nearest_atm(user_coordinates)

                new_values['$set']['user_data.lat'] = user_coordinates[0]
                new_values['$set']['user_data.long'] = user_coordinates[1]
                new_values['$set']['user_data.atm'] = nearest_atm['ATM']
                new_values['$set']['user_data.atm_name'] = nearest_atm['name']
                new_values['$set']['user_data.atm_coordinates'] = nearest_atm['coordinates']
                new_values['$set']['end_timestamp'] = datetime.datetime.now()
        else:
            chatbot.clear_sender_state(sender['sender_id'])
            chatbot.send_message(sender['sender_id'], message={
                                 'text': 'Zəhmət olmasa, hal-hazırkı yerinizi bizimlə paylaşın.'})
            return sender
    else:
        return sender

    new_values['$set']['step'] = step + 1
    return chatbot.update_sender(sender, new_values)


def send_nearest_branch(user_coordinates):
    """Return the location of the nearest branch on map object to user
    by comparing <user_coordinates> with branch coordinates.
    """
    with open("files/branch_az.json", encoding="utf-8") as branches_json:
        branches = json.load(branches_json)

    branch_to_distance = {}

    for branch in branches:
        branch_coordinates = (branch['latitude'], branch['longitude'])
        branch_to_distance[branch['id']] = calculate_haversine(
            user_coordinates, branch_coordinates)
        # sort branch_to_distance dictionary according to values (distances between user's location)
    branches_sorted_by_distance = sorted(
        branch_to_distance.items(), key=operator.itemgetter(1))

    nearest_branch_id = branches_sorted_by_distance[0][0]
    nearest_branch = {}

    for branch in branches:
        if branch['id'] == nearest_branch_id:
            nearest_branch = branch

    # create map object for facebook with yandex map image
    branch_coordinates = (
        nearest_branch['latitude'], nearest_branch['longitude'])
    image_url = "https://static-maps.yandex.ru/1.x/?lang=tr_TR&ll=" + \
        str(branch_coordinates[1]) + "," + str(branch_coordinates[0]) + \
        "&size=545,280&z=16&l=map&pt=" + str(branch_coordinates[1]) + \
        "," + str(branch_coordinates[0]) + ",round"
    item_url = "http://maps.apple.com/maps?q=" + \
        str(branch_coordinates[0]) + "," + \
        str(branch_coordinates[1]) + "&z=16"

    message = {
        'attachment': {
            'type': 'template',
            'payload': {
                    'template_type': 'generic',
                    'elements': {
                        'element': {
                            'title': nearest_branch['address_line1'],
                            'subtitle': nearest_branch['address_line1'],
                            'image_url': image_url,
                            'item_url': item_url
                        }
                    }
            }
        }
    }

    return message
