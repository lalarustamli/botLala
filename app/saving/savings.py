from app import chatbot, utils
import datetime


def cards_info_menu(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[2],
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
                        'image_url': 'https://pbs.twimg.com/profile_images/872795852724731905/OvaIBpy__400x400.jpg',
                        'subtitle': 'Standard Kart növləri',
                        'buttons':[
                            {
                                'type': 'postback',
                                'title': 'Kartlar haqqında',
                                'payload': 'standard_card_info'

                            },
                            {
                                'type': 'postback',
                                'title': 'Kart sifarişi',
                                'payload': 'credit_order_details'

                            }
                        ]
                    },
                    {
                        'title': 'Status Kartlar',
                        'image_url': 'https://pbs.twimg.com/profile_images/872795852724731905/OvaIBpy__400x400.jpg',
                        'subtitle': 'Status Kart növləri',
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Kartlar haqqında',
                                'payload': 'status_card_info'

                            },
                            {
                                'type': 'postback',
                                'title': 'Kart sifarişi',
                                'payload': 'credit_order_details'

                            }
                        ]
                    },
                    {
                        'title': 'Premium Kartlar',
                        'image_url': 'https://pbs.twimg.com/profile_images/872795852724731905/OvaIBpy__400x400.jpg',
                        'subtitle': 'Premium Kart növləri',
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Kartlar haqqında',
                                'payload': 'premium_card_info'

                            },
                            {
                                'type': 'postback',
                                'title': 'Kart sifarişi',
                                'payload': 'credit_order_details'

                            }
                        ]
                    },
                    {
                        'title': 'Ekskluziv Kartlar',
                        'image_url': 'https://pbs.twimg.com/profile_images/872795852724731905/OvaIBpy__400x400.jpg',
                        'subtitle': 'Ekskluziv Kart növləri',
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Kartlar haqqında',
                                'payload': 'exclusive_card_info'

                            },
                            {
                                'type': 'postback',
                                'title': 'Kart sifarişi',
                                'payload': 'credit_order_details'

                            }
                        ]
                    }
                ]
            }
        }
    }

    return message


