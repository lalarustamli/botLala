from app import chatbot, utils
import datetime
import json
from flask import url_for

def main_menu(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[0],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    message = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'image_aspect_ratio': 'horizontal',
                    'elements': [
                        {
                            "title": "Kart əməliyyatları",
                            "image_url": "https://i.ibb.co/0DNJyvB/Frame-1.png",
                            "subtitle": "Adi, status və virtual kartlar",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Günlük məzənnələr",
                                    "payload": "my_cards"
                                }, {
                                    "type": "postback",
                                    "title": "Ödəniş əməliyyatları",
                                    "payload": "my_cards"
                                }
                                , {
                                    "type": "postback",
                                    "title": "Online sifariş",
                                    "payload": "credit_order_details"
                                }
                            ]
                        },
                        {
                            "title": "Məhsullar",
                            "image_url": "https://i.ibb.co/KrY5gzK/Frame-3.png",
                            "subtitle": "Kartlar, kabinet və əmanətlər",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Kart məhsulları",
                                    "payload": "cards_info_menu"
                                }, {
                                    "type": "postback",
                                    "title": "Kredit məhsulları",
                                    "payload": "credits_info_menu"
                                }
                                , {
                                    "type": "postback",
                                    "title": "Depozit məhsulları",
                                    "payload": "credits_info_menu"
                                }
                            ]
                        },
                        {
                            "title": "Kreditlər",
                            "image_url": "https://i.ibb.co/XC1Yvjb/Frame-2.png",
                            "subtitle": "Kredit və depozit əməliyyatları",
                            "buttons":[
                                {
                                    "type": "postback",
                                    "title": "Kredit kalkuyatoru",
                                    "payload": "credit_calculator"
                                },
                                {
                                    "type": "postback",
                                    "title": "Depozit kalkuyatoru",
                                    "payload": "deposit_calculator"
                                },

                                {
                                    "type": "postback",
                                    "title": "Kredit sifarişi",
                                    "payload": "credit_order_details"
                                }
                            ]
                        },
                        {
                            "title": "Valyuta məzənnəsi",
                            "image_url": "https://i.ibb.co/0DNJyvB/Frame-1.png",
                            "subtitle": "Valyutalar",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Mərkəzi Bank",
                                    "payload": "cba_rates"
                                }, {
                                    "type": "postback",
                                    "title": "ABB məzənnəsi",
                                    "payload": "iba_rates"
                                }
                                , {
                                    "type": "postback",
                                    "title": "Məzənnə kalkulyatoru",
                                    "payload": "iba_rates"
                                }
                            ]
                        }
                    ]
                }
            }
        }

    return message
