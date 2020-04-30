from app import utils
from app.currency import currency
import datetime
from app import chatbot

def deposit_calculator(amount, period, frequency):
    """Return monthly or yearly payments and final amount 
    based on <frequency>, <period> and <amount>.
    """
    final_amount = 0
    yearly = 0
    monthly = 0

    if frequency == "annual":
        if period == 12:
            final_amount = amount + amount * 0.09 * 1
        elif period == 24:
            final_amount = amount + amount * 0.095 * 2
        elif period == 36:
            final_amount = amount + amount * 0.095 * 3
        else:
            raise Exception('Mövcud seçimlər: 12 , 24, 36')
        yearly = final_amount - amount

    elif frequency == "monthly":
        if period == 12:
            final_amount = amount + amount * 0.085
            monthly = (final_amount - amount) / 12
        elif period == 24:
            final_amount = amount + amount * 0.09 * 2
            monthly = (final_amount - amount) / 24
        elif period == 36:
            final_amount = amount + amount * 0.09 * 3
            monthly = (final_amount - amount) / 36
        else:
            raise Exception('Mövcud seçimlər: 12 , 24, 36')
    else:
        raise Exception('Mövcud seçimlər: illik/aylıq')

    final_amount = round(final_amount, 2)
    monthly = round(monthly, 2)
    yearly = round(yearly, 2)

    response = {'final_amount': final_amount,
                'monthly': monthly,
                'annual': yearly}

    return response


def ask_deposit_calculator_details(sender_id, step=0):
    """Return a message according to appropriate number of
    the deposit calculator state that bot should send to 
    the user with <sender_id> to collect information.
    """
    text = ""
    quick_reply = []

    if step == 0:
        text = "Depozit hesablama blokuna daxil olmusunuz." \
            "Zəhmət olmasa, botun verdiyi sualları cavablandırın." \
            "Əmanətin ümumi məbləği nə qədərdir?"

        sender = {'sender_id': sender_id,
                  'step': 0,
                  'state': chatbot.CALCULATOR_STATE[1],
                  'status': chatbot.STATE_STATUS[0],
                  'start_timestamp': datetime.datetime.now(),
                  'user_data': {}}
        chatbot.insert_sender(sender)
    elif step == 1:
        text = "Depozit müddəti neçə aydır?"
        # chatbot.bot.quick_reply(sender_id,q_text,titles=("12 ay", "24 ay", "36 ay"),
        #                                           payloads=("12", "24", "36"))
        quick_reply = chatbot.quick_reply_creator(titles=("12 ay", "24 ay", "36 ay"),
                                                  payloads=("12", "24", "36"))
    elif step == 2:
        text = "Ödənişlər aylıq yoxsa illik ödəniləcək?"
        # chatbot.bot.quick_reply(sender_id,q_text,titles=("İllik", "Aylıq"),
        #                                           payloads=("annual", "monthly"))
        quick_reply = chatbot.quick_reply_creator(titles=("İllik", "Aylıq"),
                                                   payloads=("annual", "monthly"))
    else:
        new_values = {'$set': {}}
        sender = chatbot.find_sender(sender_id, chatbot.CALCULATOR_STATE[1])
        new_values['$set']['status'] = chatbot.STATE_STATUS[2]
        chatbot.update_sender(sender, new_values)
        calulated_deposit = deposit_calculator(sender['user_data']['deposit_amount'],
                                               sender['user_data']['deposit_period'],
                                               sender['user_data']['deposit_frequency'])

        #!!!!!!!!! in here check if frequency is annual or monthly, and change text

        text = 'Ümumi məbləğ: {} AZN. Aylıq ödəniş: {} AZN. İllik ödəniş: {} AZN.'.format(calulated_deposit['final_amount'],
                    calulated_deposit['monthly'],
                    calulated_deposit['annual'])

    # chatbot.bot.send_message(sender_id,text)
    message = {
        'text': text
    }
    #
    if quick_reply:
        message['quick_replies'] = quick_reply

    return message


def save_deposit_calculator_details(sender, user_message):
    """Return updated <sender> with all information needed for a deposit calculator.
    Store required information included in <user_message> and 
    update number of steps in the database for <sender>.
    """
    step = sender['step']
    new_values = {'$set': {}}

    if step == 0:
        new_values['$set']['user_data.deposit_amount'] = float(user_message['text'])
    elif step == 1:
        if 'quick_reply' in user_message:
            new_values['$set']['user_data.deposit_period'] = int(
                user_message['quick_reply']['payload'])
        else:
            # !!!!!!!!!! check if user enters it manually
            chatbot.send_message(sender['sender_id'],
                                 message={'text': 'Zəhmət olmasa, mövcud seçimlərdən birini edin'})
            return sender
    elif step == 2:
        if 'quick_reply' in user_message:
            new_values['$set']['user_data.deposit_frequency'] = str(
                user_message['quick_reply']['payload'])
            new_values['$set']['end_timestamp'] = datetime.datetime.now()
        else:
            # !!!!!!!!!! check if user enters it manually
            chatbot.send_message(sender['sender_id'],
                                 message={'text': 'Zəhmət olmasa, mövcud seçimlərdən birini edin'})
            return sender

    else:
        return sender

    new_values['$set']['step'] = step + 1
    return chatbot.update_sender(sender, new_values)
