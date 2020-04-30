from app import chatbot
import datetime

def standard_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[0],
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
                        "title": "MasterCard Debit Standard PayPass",
                        "image_url": "https://i.ibb.co/KyQzv6W/MC-debit-standart.png",
                        "subtitle": "Standrad kart növləri",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/just-cards/mastercard-debit-standard/?utm_source=MasterCard%20Debit%20Standard%20PayPass&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "MasterCard Maestro",
                        "image_url": "https://i.ibb.co/cKW8Jch/MC-maestro.png",
                        "subtitle": "Sadə və münasib MasterCard kartı",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/just-cards/mc-maestro/?utm_source=MasterCard%20Maestro&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "VISA Classic PayWave",
                        "image_url": "https://i.ibb.co/n6KPr5T/visa-classic-paywave.png",
                        "subtitle": "VISA Classic PayWave",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/just-cards/visa-classic-paywave/?utm_source=VISA%20Classic%20PayWave&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "UnionPay Classic",
                        "image_url": "https://i.ibb.co/YDYTN5y/unionpay-classic.png",
                        "subtitle": "UnionPay Classic",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/just-cards/unionpay-classic/?utm_source=UnionPay%20Classic&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "Azercell Kobrend",
                        "image_url": "https://i.ibb.co/h9X7dTr/azercell-kobrend.png",
                        "subtitle": "UnionPay Classic",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/just-cards/az-rcell-kobrand-kart/?utm_source=Azercell%20Kobrend%20kart&utm_medium=BOT&utm_campaign=Cards_for_Bot",
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

def standard_paypass_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[0],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 10 AZN.\n" \
           "Debet rejimində işləyir.Nağd pulun əldə edilməsi, " \
           "habelə ticarət və xidmət müəssisələrində, internetdə alış-verişin aparılması üçün istifadə olunur."

    url=" https://www.ibar.az/az/individual/plastic-cards/just-cards/mastercard-debit-standard/?utm_source=MasterCard%20Debit%20Standard%20PayPass&utm_medium=BOT&utm_campaign=Cards_for_Bot"

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

def standard_maestro_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[0],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 10 AZN.\n" \
           "Debet rejimində işləyir.Nağd pulun əldə edilməsi, habelə ticarət və xidmət müəssisələrində, " \
           "internetdə alış-verişin aparılması üçün istifadə olunur."

    url="https://www.ibar.az/az/individual/plastic-cards/just-cards/mc-maestro/?utm_source=MasterCard%20Maestro&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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

def standard_paywave_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[0],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 10 AZN.\n" \
           "İstər debet, istərsə də kredit rejimində işləyə bilər." \
           "Həm nağd pulun əldə edilməsi, həm də alış-verişlərin, ödəmələrin həyata keçirilməsi üçün istifadə olunur."

    url="https://www.ibar.az/az/individual/plastic-cards/just-cards/visa-classic-paywave/?utm_source=VISA%20Classic%20PayWave&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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

def standard_union_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[0],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "1 illik xidmətin qiyməti: 10 AZN.\n" \
           "Debet və kredit rejimlərində işləyə bilər.\n" \
           "Bütün dünyada həm ATM-lərdə, həm də ticarət-xidmət nöqtələrində istifadə etmək olar."

    url="https://www.ibar.az/az/individual/plastic-cards/just-cards/unionpay-classic/?utm_source=UnionPay%20Classic&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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


def standard_azercell_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[0],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "4 illik xidmətin qiyməti: 10 AZN.\n"\
           "Azercell Kobrend kart sahibləri nağdsiz ödənişlər zamanı hər 1 AZN üçün 1 bal əldə edərək, onları şəbəkədaxili danışıq dəqiqələri və ya internet paketlərə dəyişə bilər.\n" \
           "Debet və kredit rejimlərində işləyir\n" \
           "Müddəti - 4 il\n" \
           "Cashback - 40%-dək\n" \
           "SMS xəbərdarlıq - pulsuz\n" \
           "Nağdlaşdırma - 0% (ABB ATM-lərində)"

    url="https://www.ibar.az/az/individual/plastic-cards/just-cards/az-rcell-kobrand-kart/?utm_source=Azercell%20Kobrend%20kart&utm_medium=BOT&utm_campaign=Cards_for_Bot"

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