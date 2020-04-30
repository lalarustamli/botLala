from app import chatbot
import datetime

def virtual_card_info(sender_id):
    """
    payloads:
    - visa_internet_card_info
    - master_web_card_info
    """
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[2],
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
                        "title": "VISA InternetCard",
                        "image_url": "https://i.ibb.co/0XWkjZC/visa-internet-card.png",
                        "subtitle": "1 illik xidmətin qiyməti: 4 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/e-shopping-card/visa-internetcard/?utm_source=VISA%20InternetCard&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "MasterCard WebCard",
                        "image_url": "https://i.ibb.co/jyY2fYH/MC-web-card.png",
                        "subtitle": "1 illik xidmətin qiyməti: 4 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/e-shopping-card/mc-webcard/?utm_source=MasterCard%20WebCard&utm_medium=BOT&utm_campaign=Cards_for_Bot",
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


def visa_internet_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[2],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 10 AZN .\n" \
           "Debet rejimində işləyir.\n" \
           "Nağd pulun əldə edilməsi, habelə ticarət və xidmət müəssisələrində, internetdə alış-verişin aparılması üçün istifadə olunur. " \
           "Müştəri onlayn sifariş verdiyi kartı təhvil almaq üçün filiala gəlməlidir."

    url = "https://www.ibar.az/az/individual/plastic-cards/e-shopping-card/visa-internetcard/?utm_source=VISA%20InternetCard&utm_medium=BOT&utm_campaign=Cards_for_Bot"
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": text,
                "buttons": [
                    {
                        "type": "web_url",
                        "url": url,
                        "title": "Ətraflı"
                    },
                    {
                        "type": "web_url",
                        "url": url,
                        "title": "Sifariş"
                    }
                ]
            }
        }
    }

    return message

def master_web_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[2],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 10 AZN . \n" \
           "Debet rejimində işləyir. \n" \
           "Nağd pulun əldə edilməsi, habelə ticarət və xidmət müəssisələrində, internetdə alış-verişin aparılması üçün istifadə olunur. \n" \
           "Müştəri onlayn sifariş verdiyi kartı təhvil almaq üçün filiala gəlməlidir."

    url = "https://www.ibar.az/az/individual/plastic-cards/e-shopping-card/mc-webcard/?utm_source=MasterCard%20WebCard&utm_medium=BOT&utm_campaign=Cards_for_Bot"
    message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": text,
                "buttons": [
                    {
                        "type": "web_url",
                        "url": url,
                        "title": "Ətraflı"
                    },
                    {
                        "type": "web_url",
                        "url": url,
                        "title": "Sifariş"
                    }
                ]
            }
        }
    }

    return message