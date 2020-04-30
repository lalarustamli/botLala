from app import chatbot
import datetime
from pymongo import MongoClient
import random
def subscribe(sender_id, step=0):
    """Subscribe to bot news
    """
    text = ""
    quick_reply = []
    if step == 0:
        text = "Səni çox bezdirmək istəmirəm. Bankımızın ən son yeniliklərinə "\
            "abonə olsan ilk məlumatları sən alacaqsan. Abonə olmaq istəyirsən?"\
            "(Siz abonə olmaqla FB üzərindəki məlumatlarınızı "\
            "({Name},{Age},{birthday} və s.)) bizimlə bölüşməyə razılıq verirsiniz.)"

        quick_reply = chatbot.quick_reply_creator(
            titles=("Bəli", "Xeyr"),
            payloads=(1, 0))

        sender = {'sender_id': sender_id,
                  'step': 0,
                  'state': chatbot.SUBSCRIPTION_STATE,
                  'status': chatbot.STATE_STATUS[0],
                  'start_timestamp': datetime.datetime.now(),
                  'user_data': {}}
        chatbot.insert_sender(sender)
    else:
        new_values = {'$set': {}}
        sender = chatbot.find_sender(sender_id, chatbot.SUBSCRIPTION_STATE)
        new_values['$set']['status'] = chatbot.STATE_STATUS[2]
        chatbot.update_sender(sender, new_values)
        if sender['user_data']['subscribed']:
            text = "Abonə siyahıma qoşuldunuz!"
        else:
                text = "Təşəkkür edirik! Bundan sonra yalnız seçimlərin əsasında xidmət göstərəcəm."

    message = {
        'text': text
    }

    if quick_reply:
        message['quick_replies'] = quick_reply

    return message


def save_subscription_state(sender, user_message):
    """Return updated <sender>. Store <sender> information from <user_message>
    and update step number in the database.
    """
    step = sender['step']
    new_values = {'$set': {}}

    if step == 0:
        if 'quick_reply' in user_message:
            new_values['$set']['user_data.subscribed'] = bool(
                int(user_message['quick_reply']['payload']))
            #!!!!!!!!!! add entity
            new_values['$set']['end_timestamp'] = datetime.datetime.now()
        else:
            return sender
    else:
        return sender
    new_values['$set']['step'] = step + 1
    return chatbot.update_sender(sender, new_values)


def find_subscribed_sender():
    """Helper function to return list of subscribed users
    """
    client = MongoClient(chatbot.DB_URL)
    db = client['chatbotdb']
    user_states = db['user_states']
    subscribed_users = list(user_states.find({'user_data.subscribed': True}))
    client.close()
    return subscribed_users


def send_subscription_messages(message):
    """Send message to subscribed users -- Not tested yet, needs to be edited
    """
    subscribed_users = find_subscribed_sender()
    for user in subscribed_users:
        chatbot.send_message(user['sender_id'], message)
