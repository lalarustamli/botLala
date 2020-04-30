from app import chatbot
import datetime

def credit_info_menu(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[4],
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
                        "title": "Əmək haqqı krediti",
                        "image_url": "https://i.ibb.co/0XWkjZC/visa-internet-card.png",
                        "subtitle": "",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Ətraflı",
                                "payload": "salary_loan"
                            }
                        ]
                    },
                    {
                        "title": "Pensiya krediti",
                        "image_url": "https://i.ibb.co/jyY2fYH/MC-web-card.png",
                        "subtitle": "1 illik xidmətin qiyməti: 4 AZN",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Ətraflı",
                                "payload": "pension_loans"
                            }
                        ]
                    },
                    {
                        "title": "Pensiya+",
                        "image_url": "https://i.ibb.co/jyY2fYH/MC-web-card.png",
                        "subtitle": "1 illik xidmətin qiyməti: 4 AZN",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Ətraflı",
                                "payload": "pension_plus"
                            }
                        ]
                    },
                    {
                        "title": "Kart üzrə kedit limiti",
                        "image_url": "https://i.ibb.co/jyY2fYH/MC-web-card.png",
                        "subtitle": "1 illik xidmətin qiyməti: 4 AZN",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Ətraflı",
                                "payload": "line_of_credit_card"
                            }
                        ]
                    },
                    {
                        "title": "Əmanətçi nağd krediti",
                        "image_url": "https://i.ibb.co/jyY2fYH/MC-web-card.png",
                        "subtitle": "1 illik xidmətin qiyməti: 4 AZN",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Ətraflı",
                                "payload": "depositor_loans"
                            }
                        ]
                    },
                    {
                        "title": "Əmanətçi kredit limiti",
                        "image_url": "https://i.ibb.co/jyY2fYH/MC-web-card.png",
                        "subtitle": "1 illik xidmətin qiyməti: 4 AZN",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Ətraflı",
                                "payload": "card_credit_limit"
                            }
                        ]
                    },
                    {
                        "title": "İpoteka krediti (AİF)",
                        "image_url": "https://i.ibb.co/jyY2fYH/MC-web-card.png",
                        "subtitle": "1 illik xidmətin qiyməti: 4 AZN",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Ətraflı",
                                "payload": "mortgage"
                            }
                        ]
                    },
                    {
                        "title": "MİDA ipoteka krediti",
                        "image_url": "https://i.ibb.co/jyY2fYH/MC-web-card.png",
                        "subtitle": "1 illik xidmətin qiyməti: 4 AZN",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "Ətraflı",
                                "payload": "mida"
                            }
                        ]
                    }
                ]
            }
        }
    }

    return message


def salary_loan_card(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "💸 Məbləğ: 20 000 manatadək \n" \
           "⌛ Müddət: 48 ayadək \n" \
           "📈 Faiz dərəcəsi: 20-24% \n" \
           "👪 Zamin ABB-nin kartı vasitəsilə əmək haqqı və ya pensiya alan şəxs olduğu halda: 18-22% \n" \
           "💳 Krediti əmək haqqını ABB tərəfindən buraxılmış “əmək haqqı” kartları vasitəsilə alan şəxslər ala bilər"

    url = "https://www.ibar.az/az/individual/credits/salary-loan/"
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
                        "type": "postback",
                        "title": "Kredit sifarişi",
                        "payload": "credit_order_details"
                    }
                ]
            }
        }
    }

    return message

def pension_loans_card(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "💸 Məbləğ: 20 000 manatadək \n" \
           "⌛Müddət: 60 ayadək \n" \
           "📈 Faiz dərəcəsi: 20-24% (Zamin ABB-nin kartı vasitəsilə əmək haqqı və ya pensiya alan şəxs olduğu halda: 18-22%) \n" \
           "💳 Krediti pensiyanı ABB tərəfindən buraxılmış pensiya kartları vasitəsilə alan şəxslər ala bilər \n"


    url = "https://www.ibar.az/az/individual/credits/pension-loans/"
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
                        "type": "postback",
                        "title": "Kredit sifarişi",
                        "payload": "credit_order_details"
                    }
                ]
            }
        }
    }

    return message

def pension_plus_card(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = '💸"Pensiya+"" Azərbaycan Beynəlxalq Bankının bütün pensiya kartlarının sahiblərinə minimum 100 AZN, ' \
           'maksimum pensiya məbləği qədər hər ay yenilənən faizsiz kredit limitini əldə etmək imkanı verən xidmətdir.\n' \
           'Kredit limiti pensiyaçının müraciəti əsasında artırıla bilər.\n' \
           '📈 Xidmət pulsuzdur, pensiyaçıdan heç bir əlavə komisyon haqqı və ya kredit faizi tutulmur.'

    url = "https://www.ibar.az/az/individual/credits/pension-plus/"
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
                        "type": "postback",
                        "title": "Kredit sifarişi",
                        "payload": "credit_order_details"
                    }
                ]
            }
        }
    }

    return message

def line_of_credit_card(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "💸 Məbləğ: 5 000 manatadək (VISA və ya MasterCard) \n" \
           "⌛Müddət: 12 ayadək \n" \
           "👪Təminat: Fərdi qaydada kredit məbləğindən asılı olmayaraq zaminlik tələb oluna bilər"


    url = "https://www.ibar.az/az/individual/credits/line-of-credit-card/"
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
                        "type": "postback",
                        "title": "Kredit sifarişi",
                        "payload": "credit_order_details"
                    }
                ]
            }
        }
    }

    return message


def depositor_loans_card(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "💸 Məbləğ: Əmanətin 70%-dək, əmanətin valyutasında 50 000-dək \n" \
           "📈 Faiz dərəcəsi: \n" \
           "₼ Milli valyutada - depozitin faiz dərəcəsi + 5%\n" \
           "💲 Xarici valyutada - depozitin faiz dərəcəsi + 3%\n" \
           "⌛Müddət: Depozit müddətinin sonunadək (5 ildən yuxarı olmamaq şərti ilə)"



    url = "https://www.ibar.az/az/individual/credits/depositor-loans/"
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
                        "type": "postback",
                        "title": "Kredit sifarişi",
                        "payload": "credit_order_details"
                    }
                ]
            }
        }
    }

    return message

def card_credit_limit_card(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "💸Məbləğ: Əmanətin 60%-dək, əmanətin valyutasında 50 000-dək \n" \
           "💲Valyuta: Əmanətin valyutası \n" \
           "⌛Müddət: 12 ay (depozitin müddətini keçməmək şərti ilə)"


    url = "https://www.ibar.az/az/individual/credits/card-credit-limit/"
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
                        "type": "postback",
                        "title": "Kredit sifarişi",
                        "payload": "credit_order_details"
                    }
                ]
            }
        }
    }

    return message

def mortgage_card(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "💸 Adi ipoteka kreditləri: \n" \
           "▪️Maksimal məbləğ: 150 000 AZN \n" \
           "▪️İllik faiz dərəcəsi: 8% \n" \
           "▪️Maksimal müddət: 25 il \n" \
           "▪️İlkin ödəniş: minimum 30%\n" \
           "💸 Güzəştli ipoteka kreditləri:\n" \
           "▪️Maksimal məbləğ: 100 000 AZN\n" \
           "▪️İllik faiz dərəcəsi: 4%\n" \
           "▪️Maksimal müddət: 30 il\n" \
           "▪️İlkin ödəniş: minimum 30%\n"



    url = "https://www.ibar.az/az/individual/credits/mortgage/"
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
                        "type": "postback",
                        "title": "Kredit sifarişi",
                        "payload": "credit_order_details"
                    }
                ]
            }
        }
    }

    return message

def mida_card(sender_id):
    sender = {'sender_id': sender_id,
              'state': chatbot.MENU_STATE[4],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    text = "💸 Məbləğ: 100 000 manatadək\n" \
           "⌛Müddət: 3-30 il\n" \
           "📈Faiz dərəcəsi: 4%\n" \
           "💰İlkin ödəniş: Min. 10%"



    url = "https://www.ibar.az/az/individual/credits/mida/"
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
                        "type": "postback",
                        "title": "Kredit sifarişi",
                        "payload": "credit_order_details"
                    }
                ]
            }
        }
    }

    return message