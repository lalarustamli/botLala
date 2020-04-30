from app import chatbot
import datetime

def status_card_info(sender_id):
    """
    payloads:
    - visa_gold_card_info
    - gold_maestro_card_info
    - gold_union_card_info
    - platinum_visa_card_info
    - platinum_master_card_info
    - green_american_card_info
    - gold_american_card_info
    """
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[1],
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
                        "title": "Visa Gold",
                        "image_url": "https://i.ibb.co/7rkwmgv/visa-gold.png",
                        "subtitle": "1 illik xidmət: 30 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/status-cards/visa-gold/?utm_source=VISA%20Gold&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "MasterCard Gold",
                        "image_url": "https://i.ibb.co/Ks5Wdgn/MC-gold.png",
                        "subtitle": "1 illik xidmət: 30 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/status-cards/mc-gold/?utm_source=MasterCard%20Gold&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "UnionPay Gold",
                        "image_url": "https://i.ibb.co/xsVNcRg/unionpay-gold.png",
                        "subtitle": "1 illik xidmət: 30 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/status-cards/unionpay-gold/?utm_source=UnionPay%20Gold&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "Visa Platinum",
                        "image_url": "https://i.ibb.co/1bhZMJm/visa-platinum-prime.png",
                        "subtitle": "1 illik xidmət: 50 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/status-cards/visa-platinum-card/?utm_source=VISA%20Platinum&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "MasterCard Platinum",
                        "image_url": "https://i.ibb.co/PzJvZv7/MC-platinum.png",
                        "subtitle": "1 illik xidmət: 50 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/status-cards/mc-platinum-card/?utm_source=MasterCard%20Platinum&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "UnionPay Platinum",
                        "image_url": "https://i.ibb.co/GJ87vv8/unionpay-platinum.png",
                        "subtitle": "1 illik xidmət: 60 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/status-cards/unionpay-platinum/?utm_source=UnionPay%20Platinum&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "American Express Green",
                        "image_url": "https://pbs.twimg.com/profile_images/872795852724731905/OvaIBpy__400x400.jpg",
                        "subtitle": "1 illik xidmət: 60 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/status-cards/amex-green/?utm_source=American%20Express%20Green&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "American Express Gold",
                        "image_url": "https://pbs.twimg.com/profile_images/872795852724731905/OvaIBpy__400x400.jpg",
                        "subtitle": "1 illik xidmət: 150 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/status-cards/amex-gold/?utm_source=American%20Express%20Gold&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    }
                ]
            }
        }
    }

    return message


def visa_gold_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[1],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 30 AZN." \
           "Həm debet, həm də kredit rejimində işləyə bilər." \
           "Bütün dünyada həm bankomat, həm də ticarət-xidmət nöqtələrində istifadə edə bilərsiniz."

    url="https://www.ibar.az/az/individual/plastic-cards/status-cards/visa-gold/?utm_source=VISA%20Gold&utm_medium=BOT&utm_campaign=Cards_for_Bot"

    message={
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text":text,
                "buttons":[
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Ətraflı"
                    },
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Sifariş"
                    }
                ]
            }
        }
    }

    return message

def gold_maestro_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[1],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 30 AZN." \
           "Həm debet, həm də kredit rejimində işləyə bilər." \
           "Bütün dünyada həm bankomat, həm də ticarət-xidmət nöqtələrində istifadə edə bilərsiniz."

    url="https://www.ibar.az/az/individual/plastic-cards/status-cards/mc-gold/?utm_source=MasterCard%20Gold&utm_medium=BOT&utm_campaign=Cards_for_Bot"

    message={
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text":text,
                "buttons":[
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Ətraflı"
                    },
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Sifariş"
                    }
                ]
            }
        }
    }
    return message

def gold_union_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[1],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 30 AZN." \
           "Debet və kredit rejimlərində işləyir." \
           "Bütün dünyada həm ATM-lərdə, həm də ticarət-xidmət nöqtələrində istifadə etmək olar."

    url="https://www.ibar.az/az/individual/plastic-cards/status-cards/unionpay-gold/?utm_source=UnionPay%20Gold&utm_medium=BOT&utm_campaign=Cards_for_Bot"

    message={
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text":text,
                "buttons":[
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Ətraflı"
                    },
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Sifariş"
                    }
                ]
            }
        }
    }

    return message

def platinum_visa_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[1],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 50 AZN." \
           "Həm debet, həm də kredit rejimində işləyə bilər." \
           "Bütün dünyada həm bankomat, həm də ticarət-xidmət nöqtələrində istifadə etmək olar."


    url="https://www.ibar.az/az/individual/plastic-cards/status-cards/visa-platinum-card/?utm_source=VISA%20Platinum&utm_medium=BOT&utm_campaign=Cards_for_Bot"

    message={
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text":text,
                "buttons":[
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Ətraflı"
                    },
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Sifariş"
                    }
                ]
            }
        }
    }
    return message


def platinum_master_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[1],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 50 AZN. " \
           "əm debet, həm də kredit rejimində işləyə bilər." \
           "Bütün dünyada həm bankomat, həm də ticarət-xidmət nöqtələrində istifadə edə bilərsiniz."


    url="https://www.ibar.az/az/individual/plastic-cards/status-cards/mc-platinum-card/?utm_source=MasterCard%20Platinum&utm_medium=BOT&utm_campaign=Cards_for_Bot"

    message={
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text":text,
                "buttons":[
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Ətraflı"
                    },
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Sifariş"
                    }
                ]
            }
        }
    }

    return message

def green_american_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[1],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 60 AZN." \
           "45 təqvim gününədək faizsiz kredit xətti" \
           "SMS-Xəbərdarlıq xidməti tamamilə PULSUZDUR!"

    url="https://www.ibar.az/az/individual/plastic-cards/status-cards/amex-green/?utm_source=American%20Express%20Green&utm_medium=BOT&utm_campaign=Cards_for_Bot"
    message={
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text":text,
                "buttons":[
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Ətraflı"
                    },
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Sifariş"
                    }
                ]
            }
        }
    }

    return message

def gold_american_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[1],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 150 AZN." \
           "45 təqvim gününədək faizsiz kredit xətti" \
           '"Konsyerj" proqramı'

    url="https://www.ibar.az/az/individual/plastic-cards/status-cards/amex-gold/?utm_source=American%20Express%20Gold&utm_medium=BOT&utm_campaign=Cards_for_Bot"
    message={
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"button",
                "text":text,
                "buttons":[
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Ətraflı"
                    },
                    {
                        "type": "web_url",
                        "url":url,
                        "title": "Sifariş"
                    }
                ]
            }
        }
    }

    return message