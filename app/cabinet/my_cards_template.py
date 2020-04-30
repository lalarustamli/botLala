from app import chatbot, utils
from app.cabinet import my_cards
import datetime

def my_cards_menu(sender_id,card_info):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[3],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    elems = []
    for item in card_info:
        elem={
        "title": item['cardName'],
        "image_url": "https://pbs.twimg.com/profile_images/872795852724731905/OvaIBpy__400x400.jpg",
        "subtitle": item['availableBalance'],
        "buttons": [
            {
                "type": "postback",
                "title": "Card to card",
                "payload": 'card_to_card('+str(item['cardName'])+","+str(item['cardNumber'])+')'
            }, {
                "type": "postback",
                "title": "Kart Sifarişi",
                "payload": "credit_order_details"
            }
        ]
        }
        elems.append(elem)
    message = {
        'attachment': {
            'type': 'template',
            'payload': {
                'template_type': 'generic',
                'image_aspect_ratio': 'horizontal',
                'elements': elems
            }
        }
    }

    return message


