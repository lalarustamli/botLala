from app import chatbot
import datetime

def cards_info_menu(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[1],
              'status': chatbot.STATE_STATUS[0],
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
                        'title': 'Standard Kartlar',
                        'image_url': 'https://i.ibb.co/KyQzv6W/MC-debit-standart.png',
                        'subtitle': 'Visa, MasterCard, UnionPay, Azercell',
                        'buttons':[
                            {
                                'type': 'postback',
                                'title': 'Kartlar haqqında 💳',
                                'payload': 'standard_card_info'

                            }
                        ]
                    },
                    {
                        'title': 'Status Kartlar',
                        'image_url': 'https://i.ibb.co/7rkwmgv/visa-gold.png',
                        'subtitle': 'Gold/Platinum: Visa, MasterCard, UnionPay, American Express, Yuventus',
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Kartlar haqqında 💳',
                                'payload': 'status_card_info'

                            }
                        ]
                    },
                    {
                        'title': 'Virtual kartlar',
                        'image_url': 'https://i.ibb.co/0XWkjZC/visa-internet-card.png',
                        'subtitle': 'Visa InternetCard, MasterCard WebCard',
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Kartlar haqqında 💳',
                                'payload': 'virtual_card_info'

                            }
                        ]
                    },
                    {
                        'title': 'Ekskluziv Kartlar',
                        'image_url': 'https://i.ibb.co/WpY45yC/visa-gold-prime.png',
                        'subtitle': 'Visa(Prime, Infinite), MasterCard WorldElite, American Express',
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Kartlar haqqında 💳',
                                'payload': 'exclusive_card_info'

                            }
                        ]
                    },
                    {
                        'title': 'Taksit Kartlar',
                        'image_url': 'https://i.ibb.co/fD1q6DR/tam-classic.png',
                        'subtitle': 'Tamkart (Classic/Gold/Platinum/Premium)',
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Kartlar haqqında 💳',
                                'payload': 'taksit_card_info'

                            }
                        ]
                    }
                ]
            }
        }
    }

    return message

