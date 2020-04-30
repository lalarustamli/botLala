from app import chatbot
import datetime

def exclusive_card_info(sender_id):
    """
    payloads:
    - visa_gold_prime_card_info
    - visa_platinum_prime_card_info
    - visa_infinite_card_info
    - elite_master_card_info
    - platinum_american_card_info
    """
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[3],
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
                        "title": "Visa Gold Prime",
                        "image_url": "https://i.ibb.co/WpY45yC/visa-gold-prime.png",
                        "subtitle": "1 illik xidmət: 100 AZN",
                        "buttons": [ {
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/preference-cards/visa-gold-prime/?utm_source=VISA%20Gold%20Prime&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "VISA Platinum Prime",
                        "image_url": "https://i.ibb.co/1bhZMJm/visa-platinum-prime.png",
                        "subtitle": "1 illik xidmət: 250 AZN",
                        "buttons": [ {
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/preference-cards/visa-platinum-prime/?utm_source=VISA%20Platinum%20Prime&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "VISA Infinite",
                        "image_url": "https://i.ibb.co/8MXWJBc/visa-infinite.png",
                        "subtitle": "1 illik xidmət: 350 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/preference-cards/visa-infinite/?utm_source=VISA%20Infinite&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "MasterCard World Elite",
                        "image_url": "https://i.ibb.co/znVQPHJ/MC-word-elite.png",
                        "subtitle": "1 illik xidmət: 350 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/preference-cards/mc-worldelite/?utm_source=MasterCard%20WorldElite&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "American Express Platinum",
                        "image_url": "https://pbs.twimg.com/profile_images/872795852724731905/OvaIBpy__400x400.jpg",
                        "subtitle": "1 illik xidmət: 600 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/preference-cards/visa-platinum-prime/?utm_source=VISA%20Platinum%20Prime&utm_medium=BOT&utm_campaign=Cards_for_Bot",
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


def visa_gold_prime_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[3],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = '1 illik xidmətin qiyməti: 100 AZN. \n' \
           'Nağdsız ödənişlər zamanı məbləğin 0.5%-inin müştərinin kartına qaytarılması (VISA Rewards proqramı) \n' \
           'Təmassız ödəniş  - VISA PayWave texnologiyası'

    url = "https://www.ibar.az/az/individual/plastic-cards/preference-cards/visa-gold-prime/?utm_source=VISA%20Gold%20Prime&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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

def visa_platinum_prime_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[3],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = '1 illik xidmətin qiyməti: 250 AZN.\n' \
           'Nağdsız ödənişlər zamanı məbləğin 0.5%-inin müştərinin kartına qaytarılması (VISA Rewards proqramı) \n' \
           'Təmassız ödəniş  - VISA PayWave texnologiyası'

    url = "https://www.ibar.az/az/individual/plastic-cards/preference-cards/visa-platinum-prime/?utm_source=VISA%20Platinum%20Prime&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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

def visa_infinite_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[3],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = '1 illik xidmətin qiyməti: 350 AZN.\n' \
           'Nağdsız ödənişlər zamanı məbləğin 0.5%-inin müştərinin kartına qaytarılması (VISA Rewards proqramı)\n' \
           'Pulsuz Priority Pass\n' \
           '45 təqvim gününədək faizsiz kredit xətti'


    url = "https://www.ibar.az/az/individual/plastic-cards/preference-cards/visa-infinite/?utm_source=VISA%20Infinite&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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

def elite_master_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[3],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = '1 illik xidmətin qiyməti: 350 AZN.' \
           'Yüksək məbləğdə kredit limiti' \
           '45 təqvim gününədək faizsiz kredit xətti'

    url = "https://www.ibar.az/az/individual/plastic-cards/preference-cards/mc-worldelite/?utm_source=MasterCard%20WorldElite&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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

def platinum_american_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[3],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = '1 illik xidmətin qiyməti: 600 AZN.' \
           '45 təqvim gününədək faizsiz kredit xətti' \
           'Pulsuz Priority Pass'

    url = "https://www.ibar.az/az/individual/plastic-cards/preference-cards/amex-platinum/?utm_source=American%20Express%20Platinum&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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