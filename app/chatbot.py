import requests
import datetime
import credentials as cr
from pymongo import MongoClient, ReturnDocument
from app import utils,subscribe
from app.cabinet import my_cards, my_cards_template
from app.card import cards, exclusive_card,standard_card,status_card,taksit_card,virtual_card
from app.credit import credit, credits_menu
from app.currency import currency, currency_calculator
from app.location import location
from app.menu import menu
from app.saving import deposit, savings
from app.library import Bot, MongoDB, GenericElement


API = "https://graph.facebook.com/v5.0/me/messages"

TOKEN=cr.TOKEN
DB_URL = cr.DB_URL
bot=Bot(token=TOKEN)
db=MongoDB()
CREDIT_ORDER_STATE = 'credit_order'
CURRENCY_STATE = ['conversion_rates','iba_rates','cba_rates']
SUBSCRIPTION_STATE = 'subscription'
LOCATION_STATE = ['branch_location', 'atm_location',
                  'cashin_location', 'subbranch_location']
CALCULATOR_STATE = ['credit_calculator', 'deposit_calculator']
STATE_STATUS = ['PENDING', 'WAITING_APPROVAL', 'COMPLETED']
CARD_STATE=['STANDARD','STATUS','VIRTUAL','EXCLUSIVE','TAKSIT']
MENU_STATE = ['MAIN_MENU','CARDS_MENU','SAVINGS_MENU','MYCARDS_MENU','CREDITS_MENU']
MY_CARDS_STATE='my_cards'
CARD_TO_CARD_STATE='card_to_card'

buttons1 = [
                                {
                                    "type": "postback",
                                    "title": "Günlük məzənnələr",
                                    "payload": "iba_rates"
                                }, {
                                    "type": "postback",
                                    "title": "Valyuta kalkulyatoru",
                                    "payload": "iba_rates"
                                }
                                , {
                                    "type": "postback",
                                    "title": "Mərkəzi Bank valyuta məzənnələri",
                                    "payload": "cba_rates"
                                }
                            ]

elems=[{                    "title": "Valyuta məzənnələri",
                            "image_url": "https://i.ibb.co/6Jbh2XZ/Valyuta-m-z-nn-si.png",
                            "subtitle": "Adi, status və virtual kartlar",
                            "buttons": buttons1
                        },
                        {
                            "title": "Kartlar",
                            "image_url": "https://i.ibb.co/88pF3GD/Kartlar-00000003.png",
                            "subtitle": "Kartlar, kabinet və əmanətlər",
                            "buttons": buttons1
                        }]



def verify_webhook(req):
    """Return the challenge token from the request if token is valid.
    """
    if req.args.get('hub.verify_token') == "ibarchatbot":
        return req.args.get('hub.challenge')
    else:
        return "wrong token"


def is_user_message(event):
    """Return whether the message is from the user.
    """
    return (event.get('message') and not event['message'].get("is_echo"))

def is_user_postback(event):
    return (event.get('postback'))


def respond(event):
    """Formulate a response to the user and pass it on to a send_message function.
    """
    sender_id = event['sender']['id']
    user_message = event['message']
    message = get_bot_response(sender_id, user_message)
    send_message(sender_id, message)

def postback_response(event):
    recipient_id=event['recipient']['id']
    sender_id = event['sender']['id']
    user_message = event['postback']
    message = payload_response(sender_id, user_message,recipient_id)
    send_message(sender_id, message)

def payload_response(sender_id,user_message, recipient_id):
    if user_message:

        print(user_message['payload'])
        if str(user_message['payload']).startswith('card_to_card'):
            deb=str(user_message['payload'])[13:-1]
            debitors=deb.split(',')
            debitor_num=debitors[1]
            debitor_name=debitors[0]
            sender = {'sender_id': sender_id,
                      'state': CARD_TO_CARD_STATE,
                      'step':1,
                      'status': STATE_STATUS[0],
                      'start_timestamp': datetime.datetime.now(),
                      'user_data': {
                          'debit_name':debitor_name,
                          'debit_number':debitor_num
                      }}
            db.insert_sender(sender)
            return my_cards.ask_card_to_card_info(sender_id)
        user_message=str(user_message['payload'])
        check_entity = check_entity_to_function(user_message)
        # check if entity exists
        if check_entity[0]:
            # clear user's unfinished state
            db.clear_sender_state(sender_id)
            # return proper function
            return check_entity[1](sender_id)

        # check if sender is in state
        if sender_has_state(sender_id)[0]:
            # return sender id
            sender = db.sender_has_state(sender_id)[1]
            return get_user_unfinished_state(sender, user_message)
    elif user_message.get('attachments') and user_message['attachments'][0]['type'] == "location":
        sender = find_sender(sender_id, LOCATION_STATE[1])
        sender = location.save_location_from_user(sender, user_message)
        return location.ask_location_from_user(sender_id, sender['step'])
    else:
        # !!!!! need to do some default error message
        message = {
            'text': 'hi, u send: '
        }
        return message


def get_bot_response(sender_id, user_message):
    """Return proper state function according for <sender_id>
    by analyzing <user_message>.
    """
    # check if user's message is text
    if user_message.get('text'):
        # assign entity and value of user message to wit nlp
        entity, value = utils.wit_response(user_message['text'])
        check_entity = check_entity_to_function(entity)

        # check if entity exists
        if check_entity[0]:
            # clear user's unfinished state
            db.clear_sender_state(sender_id)
            # return proper function
            return check_entity[1](sender_id)
        # check if sender is in state
        if sender_has_state(sender_id)[0]:
            # return sender id
            try:
                sender = db.sender_has_state(sender_id)[1]
                return get_user_unfinished_state(sender, user_message)
            except:
                bot.send_message(sender_id,"Düz eləmədin...")

        else:
            bot.send_generic_template(sender_id,elems)
            # text='Hal-hazırda botla danışırsınız. Menu-ya keçid edə və ya canlı əlaqəyə qoşula bilərsiniz'
            # bot.send_button_template(sender_id,
            #                          text,
            #                          types=("postback","postback"),
            #                          titles=("Menu","canli"),
            #                          urls=(None,None),
            #                          payloads=("menu","live_message"))

    elif user_message.get('attachments') and user_message['attachments'][0]['type'] == "location":
        sender = find_sender(sender_id, LOCATION_STATE[1])
        sender = location.save_location_from_user(sender, user_message)
        return location.ask_location_from_user(sender_id, sender['step'])
    else:
        #!!!!! need to do some default error message
        message = {
            'text': 'hi, u send: '
        }
        return message


def check_entity_to_function(entity):
    """Return whether <entity> contains keyword, and
    state function mapped to that entity.
    """
    credit_details_entity = "credit_order_details"
    credit_calculator_entity = "credit_calculator"
    deposit_calculator_entity = "deposit_calculator"
    location_atm_entity = "ask_atm_location"
    location_branch_entity = "ask_atm_location"
    subscription_entity = "subscription"
    iba_rates_entity = "iba_rates"
    cbar_rates_entity = "cba_rates"
    menu_entity = "menu"
    my_cards_entity="my_cards"
    cards_info_menu_entity = "cards_info_menu"
    standard_card_entity="standard_card_info"
    standard_paypass_card_entity="standard_paypass_card_info"
    standard_maestro_card_entity="standard_maestro_card_info"
    standard_paywave_card_entity="standard_paywave_card_info"
    standard_union_card_entity = "standard_union_card_info"
    standard_azercell_card_entity="standard_azercell_card_info"
    status_card_entity = "status_card_info"
    visa_gold_card_entity="visa_gold_card_info"
    gold_maestro_card_entity="gold_maestro_card_info"
    gold_union_card_entity="gold_union_card_info"
    platinum_visa_card_entity="platinum_visa_card_info"
    platinum_master_card_entity="platinum_master_card_info"
    green_american_card_entity="platinum_master_card_info"
    gold_american_card_entity="platinum_master_card_info"
    virtual_card_entity = "virtual_card_info"
    visa_internet_card_entity="visa_internet_card_info"
    master_web_card_entity="master_web_card_info"
    exclusive_card_entity = "exclusive_card_info"
    visa_gold_prime_card_entity="visa_gold_prime_card_info"
    visa_platinum_prime_card_entity="visa_platinum_prime_card_info"
    visa_infinite_card_entity="visa_infinite_card_info"
    elite_master_card_entity="elite_master_card_info"
    platinum_american_card_entity="platinum_american_card_info"
    taksit_card_entity = "taksit_card_info"
    classic_tam_card_entity="classic_tam_card_info"
    gold_tam_card_entity="gold_tam_card_info"
    platinum_tam_card_entity="platinum_tam_card_info"
    premium_tam_card_entity="premium_tam_card_info"
    savings_info_menu_entity="savings_info_menu"
    credits_info_menu_entity="credits_info_menu"
    salary_loan_entity="salary_loan"
    pension_loans_entity = "pension_loans"
    pension_plus_entity="pension_plus"
    line_of_credit_card_entity="line_of_credit_card"
    depositor_loans_entity="depositor_loans"
    card_credit_limit_entity="card_credit_limit"
    mortgage_entity="mortgage"
    mida_entity="mida"


    card_to_card_entity='card_to_card'



    # mapping entities to functions
    entity_to_function = {}
    entity_to_function[credit_calculator_entity] = credit.ask_credit_calculator_details
    entity_to_function[deposit_calculator_entity] = deposit.ask_deposit_calculator_details
    entity_to_function[credit_details_entity] = credit.ask_credit_details
    entity_to_function[location_atm_entity] = location.ask_location_from_user
    entity_to_function[location_branch_entity] = location.ask_location_from_user
    entity_to_function[subscription_entity] = subscribe.subscribe
    entity_to_function[iba_rates_entity] = currency.ask_iba_currency_calculator_details
    entity_to_function[cbar_rates_entity] = currency.get_currencies_from_cbar
    entity_to_function[menu_entity] = menu.main_menu
    entity_to_function[cards_info_menu_entity] = cards.cards_info_menu
    entity_to_function[standard_card_entity] = standard_card.standard_card_info
    entity_to_function[standard_paypass_card_entity] = standard_card.standard_paypass_card_info
    entity_to_function[standard_maestro_card_entity] = standard_card.standard_maestro_card_info
    entity_to_function[standard_paywave_card_entity] = standard_card.standard_paywave_card_info
    entity_to_function[standard_union_card_entity] = standard_card.standard_union_card_info
    entity_to_function[standard_azercell_card_entity]=standard_card.standard_azercell_card_info
    entity_to_function[status_card_entity] = status_card.status_card_info
    entity_to_function[visa_gold_card_entity]=status_card.visa_gold_card_info
    entity_to_function[gold_maestro_card_entity]=status_card.gold_maestro_card_info
    entity_to_function[gold_union_card_entity]=status_card.gold_union_card_info
    entity_to_function[platinum_visa_card_entity]=status_card.platinum_visa_card_info
    entity_to_function[platinum_master_card_entity]=status_card.platinum_master_card_info
    entity_to_function[green_american_card_entity]=status_card.green_american_card_info
    entity_to_function[gold_american_card_entity]=status_card.gold_american_card_info
    entity_to_function[virtual_card_entity] = virtual_card.virtual_card_info
    entity_to_function[visa_internet_card_entity]=virtual_card.visa_internet_card_info
    entity_to_function[master_web_card_entity]=virtual_card.master_web_card_info
    entity_to_function[exclusive_card_entity] = exclusive_card.exclusive_card_info
    entity_to_function[visa_gold_prime_card_entity]=exclusive_card.visa_gold_prime_card_info
    entity_to_function[visa_platinum_prime_card_entity]=exclusive_card.visa_platinum_prime_card_info
    entity_to_function[visa_infinite_card_entity]=exclusive_card.visa_infinite_card_info
    entity_to_function[elite_master_card_entity]=exclusive_card.elite_master_card_info
    entity_to_function[platinum_american_card_entity]=exclusive_card.platinum_american_card_info
    entity_to_function[taksit_card_entity] = taksit_card.taksit_card_info
    entity_to_function[classic_tam_card_entity]=taksit_card.classic_tam_card_info
    entity_to_function[gold_tam_card_entity] = taksit_card.gold_tam_card_info
    entity_to_function[platinum_tam_card_entity] = taksit_card.platinum_tam_card_info
    entity_to_function[premium_tam_card_entity] = taksit_card.premium_tam_card_info
    entity_to_function[my_cards_entity] = my_cards.ask_card_info
    entity_to_function[savings_info_menu_entity] = savings.cards_info_menu
    entity_to_function[card_to_card_entity]=my_cards.ask_card_to_card_info
    entity_to_function[credits_info_menu_entity]=credits_menu.credit_info_menu
    entity_to_function[salary_loan_entity]=credits_menu.salary_loan_card
    entity_to_function[pension_loans_entity]=credits_menu.pension_loans_card
    entity_to_function[pension_plus_entity] = credits_menu.pension_plus_card
    entity_to_function[line_of_credit_card_entity]=credits_menu.line_of_credit_card
    entity_to_function[depositor_loans_entity]=credits_menu.depositor_loans_card
    entity_to_function[card_credit_limit_entity]=credits_menu.card_credit_limit_card
    entity_to_function[mortgage_entity]=credits_menu.mortgage_card
    entity_to_function[mida_entity]=credits_menu.mida_card

    if entity in entity_to_function:
        return True, entity_to_function[entity]
    return False, None


def clear_sender_state(sender_id):
    """Remove <sender_id> current state with PENDING status from the database.
    """
    client = MongoClient(DB_URL)
    db = client['chatbotdb']
    user_states = db['user_states']
    user_states.delete_one(
        {'sender_id': sender_id, 'status': STATE_STATUS[0]})
    client.close()


def sender_has_state(sender_id):
    """Return whether <sender_id> has a pending state, and sender object from the database.
    """
    client = MongoClient(DB_URL)
    db = client['chatbotdb']
    user_states = db['user_states']
    sender = user_states.find_one(
        {'sender_id': sender_id, 'status': STATE_STATUS[0]})
    client.close()
    if sender:
        return True, sender
    return False, None


def get_user_unfinished_state(sender, user_message):
    """Return relevant function according to sender <state>.
    """
    # check if user is in credit calculator state
    sender_id = sender['sender_id']
    if sender['state'] == SUBSCRIPTION_STATE:
        sender = subscribe.save_subscription_state(sender, user_message)
        return subscribe.subscribe(sender_id, sender['step'])
    elif sender['state'] == CURRENCY_STATE[0]:
        sender = currency.save_iba_currency_calculator(sender, user_message)
        return currency.ask_iba_currency_calculator_details(sender_id, sender['step'])
    # credit calculator state
    elif sender['state'] == CALCULATOR_STATE[0]:
        sender = credit.save_credit_calculator_details(sender, user_message)
        return credit.ask_credit_calculator_details(sender_id, sender['step'])
    elif sender['state'] == MENU_STATE[0]:
        # sender=menu.save_menu_payloads(sender,user_message)
        return menu.main_menu(sender_id)
    elif sender['state'] == MENU_STATE[1]:
        # sender=menu.save_menu_payloads(sender,user_message)
        return cards.cards_info_menu(sender_id)
    elif sender['state'] == MENU_STATE[2]:
        return savings.cards_info_menu(sender_id)
    elif sender['state'] == MENU_STATE[4]:
        return credits_menu.credit_info_menu(sender_id)
    # # deposit calculator state
    elif sender['state'] == CALCULATOR_STATE[1]:
        sender = deposit.save_deposit_calculator_details(sender, user_message)
        return deposit.ask_deposit_calculator_details(sender_id, sender['step'])
    elif sender['state'] == CREDIT_ORDER_STATE:
        sender = credit.save_credit_details(sender, user_message)
        return credit.ask_credit_details(sender_id, sender['step'])
    elif sender['state'] == CARD_STATE[0]:
        return standard_card.standard_card_info(sender_id)
    elif sender['state'] == CARD_STATE[1]:
        return cards.status_card_info(sender_id)
    elif sender['state'] == CARD_STATE[2]:
        return virtual_card.virtual_card_info(sender_id)
    elif sender['state'] == CARD_STATE[3]:
        return exclusive_card.exclusive_card_info(sender_id)
    elif sender['state'] == CARD_STATE[4]:
        return taksit_card.taksit_card_info(sender_id)
    elif sender['state'] == CURRENCY_STATE[2]:
        return currency.get_currencies_from_cbar(sender_id)
    # atm location state
    elif sender['state'] == LOCATION_STATE[1]:
        sender = location.save_location_from_user(sender, user_message)
        return location.ask_location_from_user(sender_id, sender['step'])
    elif sender['state'] == MY_CARDS_STATE:
        sender = my_cards.save_my_cards_state(sender,user_message)
        return my_cards.ask_card_info(sender_id,sender['step'])
    elif sender['state'] == CARD_TO_CARD_STATE:
        sender = my_cards.save_card_to_card_state(sender,user_message)
        return my_cards.ask_card_to_card_info(sender_id,sender['step'])



def insert_sender(sender):
    """Insert <sender> object to the database.
    """
    client = MongoClient(DB_URL)
    db = client['chatbotdb']
    user_states = db['user_states']
    user_states.insert_one(sender)
    client.close()


def update_sender(sender, new_values):
    """Update <sender> object with <new_values> in the database.
    """
    client = MongoClient(DB_URL)
    db = client['chatbotdb']
    user_states = db['user_states']
    updated_sender = user_states.find_one_and_update(
        sender, new_values, return_document=ReturnDocument.AFTER)
    client.close()
    return updated_sender


def find_sender(sender_id, state):
    """Return sender object from the database with <sender_id>.
    """
    client = MongoClient(DB_URL)
    db = client['chatbotdb']
    user_states = db['user_states']
    updated_sender = user_states.find_one({'sender_id': sender_id, 'state': state, 'status': STATE_STATUS[0]})
    client.close()
    return updated_sender

def find_finished_sender(sender_id, state):
    """Return sender object from the database with <sender_id>.
    """
    client = MongoClient(DB_URL)
    db = client['chatbotdb']
    user_states = db['user_states']
    updated_sender = user_states.find_one({'sender_id': sender_id, 'state': state, 'status': STATE_STATUS[2]})
    client.close()
    return updated_sender


def quick_reply_creator(titles, payloads):
    """Return facebook quick reply based on <titles> and <payloads>.
    """
    quick_reply = []
    for title, payload in zip(titles, payloads):
        quick_reply.append({
            "content_type": "text",
            "title": title,
            "payload": payload
        })

    return quick_reply


def send_message(recipient_id, message):
    """Send a response to Facebook by making a post request.
    """
    payload = {
        'message': message,
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': TOKEN
    }

    response = requests.post(
        API,
        params=auth,
        json=payload
    )
    print('payload2'+str(payload))
    return response.json()

def send_image(recipient_id, url):
    payload = {
        'message': {
            'attachment': {
            'type':'template',
            'payload': {
                'template_type':'media',
                'elements': [
                    {
                        'media_type':'image',
                        'url':url
                     }
                    ]
                }
            }
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }
    auth = {
        'access_token': TOKEN
    }

    response = requests.post(
        API,
        params=auth,
        json=payload
    )

    return response.json()




def live_message(recipient_id):
    """Send a response to Facebook by making a post request.
    """
    print("LIVE")
    payload = {
        'recipient': {
            'id': recipient_id
        },
        'target_app_id':263902037430900,
        'metadata':'HELP',
        'notification_type': 'regular'
    }

    auth = {
        'access_token': TOKEN
    }
    API="https://graph.facebook.com/v2.6/me/pass_thread_control"

    response = requests.post(
        API,
        params=auth,
        json=payload
    )

    return response.json()

def live_bot(recipient_id):
    """Send a response to Facebook by making a post request.
    """
    print("BOT")
    payload = {
        'recipient': {
            'id': recipient_id
        },
        'target_app_id':cr.TARGET_ID,
        'metadata':'HELP',
        'notification_type': 'regular'
    }

    auth = {
        'access_token': TOKEN
    }
    API="https://graph.facebook.com/v2.6/me/take_thread_control"

    response = requests.post(
        API,
        params=auth,
        json=payload
    )

    return response.json()





