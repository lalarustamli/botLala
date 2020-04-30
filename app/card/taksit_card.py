from app import chatbot
import datetime

def taksit_card_info(sender_id):
    """
    payloads:
    - classic_tam_card_info
    - gold_tam_card_info
    - platinum_tam_card_info
    - premium_tam_card_info
    """
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[4],
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
                        "title": "Tamkart Classic",
                        "image_url": "https://i.ibb.co/fD1q6DR/tam-classic.png",
                        "subtitle": "Qiymət 20 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/taksit-kartlar/tamkart-classic/?utm_source=Tamkart%20Classic&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "Tamkart Gold",
                        "image_url": "https://i.ibb.co/pXgck2m/tam-gold.png",
                        "subtitle": "Qiymət 30 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/taksit-kartlar/tamkart-gold/?utm_source=Tamkart%20Gold&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "Tamkart Platinum",
                        "image_url": "https://i.ibb.co/N7RYMSD/tam-platinum.png",
                        "subtitle": "Qiymət 100 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/taksit-kartlar/tamkart-platinum/?utm_source=Tamkart%20Platinum&utm_medium=BOT&utm_campaign=Cards_for_Bot",
                                "messenger_extensions": "true",
                                "webview_height_ratio": "full"
                            }
                        ]
                    },
                    {
                        "title": "Tamkart Premium",
                        "image_url": "https://pbs.twimg.com/profile_images/872795852724731905/OvaIBpy__400x400.jpg",
                        "subtitle": "Qiymət: 300 AZN",
                        "buttons": [{
                                "type": "web_url",
                                "title": "Kart Sifarişi",
                                "url": "https://www.ibar.az/az/individual/plastic-cards/taksit-kartlar/tamkart-premium/?utm_source=Tamkart%20Premium&utm_medium=BOT&utm_campaign=Cards_for_Bot",
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


def classic_tam_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text ='Qiymət: 20 AZN\n' \
          'Çox funksiyalı tam kartın ön tərəfi kredit, arxa tərəfi isə debet kartıdır\n' \
          '18 ayadək taksit imkanı\n' \
          'Hər ödənişdə 2% cashback*\n' \
          '* Taksit əməliyyatları, kommunal ödənişlər, mobil operator ödənişləri, kart transfer, unique cash, Quasi cash ödənişləri zamanı cashback hesablanmır'

    url = "https://www.ibar.az/az/individual/plastic-cards/taksit-kartlar/tamkart-classic/?utm_source=Tamkart%20Classic&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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

def gold_tam_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = 'Qiymət: 30 AZN.\n' \
           'Çox funksiyalı tam kartın ön tərəfi kredit, arxa tərəfi isə debet kartıdır\n' \
           '18 ayadək taksit imkanı\n' \
           'Hər ödənişdə 2% cashback*\n' \
           '* Taksit əməliyyatları, kommunal ödənişlər, mobil operator ödənişləri, kart transfer, unique cash, Quasi cash ödənişləri zamanı cashback hesablanmır'


    url = "https://www.ibar.az/az/individual/plastic-cards/taksit-kartlar/tamkart-gold/?utm_source=Tamkart%20Gold&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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

def platinum_tam_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = 'Qiymət: 100 AZN.' \
           'Çox funksiyalı tam kartın ön tərəfi kredit, arxa tərəfi isə debet kartıdır\n' \
           '18 ayadək taksit imkanı\n' \
           'Hər ödənişdə 2% cashback*\n' \
           '* Taksit əməliyyatları, kommunal ödənişlər, mobil operator ödənişləri, kart transfer, unique cash, Quasi cash ödənişləri zamanı cashback hesablanmır'
    url = "https://www.ibar.az/az/individual/plastic-cards/taksit-kartlar/tamkart-platinum/?utm_source=Tamkart%20Platinum&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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

def premium_tam_card_info(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.CARD_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = 'Qiymət: 300 AZN.\n' \
           'Çox funksiyalı tam kartın ön tərəfi kredit, arxa tərəfi isə debet kartıdır\n' \
           '18 ayadək taksit imkanı\n' \
           'Hər ödənişdə 2% cashback*\n' \
           '* Taksit əməliyyatları, kommunal ödənişlər, mobil operator ödənişləri, kart transfer, unique cash, Quasi cash ödənişləri zamanı cashback hesablanmır'

    url = "https://www.ibar.az/az/individual/plastic-cards/taksit-kartlar/tamkart-premium/?utm_source=Tamkart%20Premium&utm_medium=BOT&utm_campaign=Cards_for_Bot"
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