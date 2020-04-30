from app import chatbot, utils
import datetime
import numpy
from string import Template


def credit_calculator(assurance, months, amount):
    """Return monthly and final amount based on <assurance>, <months>, <amount>.
    """
    if assurance:
        monthly = -numpy.pmt(0.23 / 12, months, amount)
    else:
        monthly = -numpy.pmt(0.25 / 12, months, amount)

    final_amount = round(monthly * months, 2)
    monthly = round(monthly, 2)

    response = {"final_amount": final_amount, "monthly": monthly}

    return response


def ask_credit_calculator_details(sender_id, step=0):
    """Return a message according to appropriate <step> number of the credit 
    calculator state that bot should send to the user with <sender_id>
    to collect information.
    """
    text = ""
    quick_reply = []

    if step == 0:
        text = "Kredit hesablama blokuna daxil oldunuz." \
            "Zəhmət olmasa, botun verdiyi sualları cavablayın." \
            "Kredit təminatlıdır?"

        quick_reply = chatbot.quick_reply_creator(
            titles=("Təminatlıdır", "Təminatlı deyil"),
            payloads=(1, 0))

        sender = {'sender_id': sender_id,
                  'step': 0,
                  'state': chatbot.CALCULATOR_STATE[0],
                  'status': chatbot.STATE_STATUS[0],
                  'start_timestamp': datetime.datetime.now(),
                  'user_data': {}}
        chatbot.insert_sender(sender)
    elif step == 1:
        text = "Kredit müddəti neçə aydır?"
    elif step == 2:
        text = "Kredit məbləği nə qədərdir?"
    elif step == 3:
        sender = chatbot.find_sender(sender_id, chatbot.CALCULATOR_STATE[0])
        response_details = {
            'final_amount': sender['user_data']['credit_final_amount'],
            'monthly': sender['user_data']['credit_monthly']
        }

        text = "Kreditin ümumi məbləği: {} AZN. Aylıq ödənişlər: {} AZN.".format(
            response_details['final_amount'], response_details['monthly'])
        # redirect to credit order
        text += "\nKredit sifariş vermək istəyirsiniz?"
        quick_reply = chatbot.quick_reply_creator(titles=("Bəli", "Xeyr"),
                                                  payloads=(1, 0))
    else:
        new_values = {'$set': {}}
        sender = chatbot.find_sender(sender_id, chatbot.CALCULATOR_STATE[0])
        new_values['$set']['status'] = chatbot.STATE_STATUS[2]
        chatbot.update_sender(sender, new_values)
        if sender['user_data']['credit_order']:
            text = "Təşəkkürlər. Sizi kredit sifarişinə yönləndiririk."
            #!!!!!!!! need to redirect ask_credit_details !!!!!!!!
            return ask_credit_details(sender_id)
        else:
            text = "Kredit kalkulyatorundan istifadə etdiyiniz üçün təşəkkürlər."

    message = {
        'text': text
    }

    if quick_reply:
        message['quick_replies'] = quick_reply

    return message


def save_credit_calculator_details(sender, user_message):
    """Return updated <sender> with all information needed for a credit 
    calculator. Store all required information included in <user_message> and 
    update number of steps in the database for <sender>.
    """
    step = sender['step']
    new_values = {'$set': {}}

    entity, value = utils.wit_response(user_message)

    if step == 0:
        if 'quick_reply' in user_message:
            new_values['$set']['user_data.credit_assurance'] = \
                bool(int(user_message['quick_reply']['payload']))
        elif entity == "confirmation":
            if value == "yes":
                new_values['$set']['user_data.credit_assurance'] = True
            else:
                new_values['$set']['user_data.credit_assurance'] = False
        else:
            chatbot.send_message(sender['sender_id'], message={
                                 'text': 'Zəhmət olmasa, mövcud seçimlərdən birini edin'})
            chatbot.clear_sender_state(sender['sender_id'])
            return sender
    elif step == 1:
        new_values['$set']['user_data.credit_months'] = int(user_message['text'])
    elif step == 2:
        new_values['$set']['user_data.credit_amount'] = int(user_message['text'])

        # calculate credit
        calculated_credit = credit_calculator(sender['user_data']['credit_assurance'],
                                              sender['user_data']['credit_months'],
                                              int(user_message['text']))

        # store results
        new_values['$set']['user_data.credit_monthly'] = calculated_credit['monthly']
        new_values['$set']['user_data.credit_final_amount'] = calculated_credit['final_amount']
    elif step == 3:
        if 'quick_reply' in user_message:
            new_values['$set']['user_data.credit_order'] = \
                bool(int(user_message['quick_reply']['payload']))
        elif entity == "confirmation":
            if value == "yes":
                new_values['$set']['user_data.credit_order'] = True
            else:
                new_values['$set']['user_data.credit_order'] = False
        else:
            chatbot.send_message(sender['sender_id'], message={
                                 'text': 'Zəhmət olmasa, mövcud seçimlərdən birini edin'})
            return sender
        new_values['$set']['end_timestamp'] = datetime.datetime.now()
    else:
        return sender

    new_values['$set']['step'] = step + 1
    return chatbot.update_sender(sender, new_values)


#========== REMOVE ===========#
# def ask_order_credit_from_calculator(sender, step=0):
    # """Return a message according to appropriate <step> number of the order
    # credit from credit calculator state that bot should send to the <sender>
    # to collect information.
    # """
    #text = ""
    #quick_reply = []

    # if step == 0:
        #text = "Kredit sifariş vermək istəyirsiniz?"
        # quick_reply = chatbot.quick_reply_creator(titles=("Bəli", "Xeyr"),
                                                  # payloads=(1, 0))
    # elif step == 1:
        #sender = chatbot.find_sender(sender_id)
        # if sender['user_data']['credit_order']:
            #text = "Təşəkkürlər1"
    # else:
        #text = "Təşəkkürlər"

    # message = {
        # 'text': text
    # }
    # if quick_reply:
        # message = {
            # 'text': text,
            # 'quick_replies': quick_reply
        # }
    # return message


# def save_order_credit_from_calculator(sender, user_message):
    # """Return updated <sender> from credit calculator state with the information
    # whether <sender> wants to order credit. Store required information included
    # in <user_message> and update number of steps in the database for <sender>.
    # """
    #step = sender['step']
    #new_values = {'$set': {}}

    #entity, value = utils.wit_response(user_message)

    # if step == 0:
        # if 'quick_reply' in user_message:
            # new_values['$set']['user_data.credit_order'] = \
                # bool(int(user_message['quick_reply']['payload']))
        # elif entity == "confirmation":
            # if value == "yes":
                #new_values['$set']['user_data.credit_order'] = True
            # else:
                #new_values['$set']['user_data.credit_order'] = False
        # else:
            # chatbot.send_message(sender['sender_id'],
                                 # message={
                                     # 'text': 'Zəhmət olmasa, mövcud seçimlərdən birini edin'
            # })
            # return sender
        #new_values['$set']['status'] = chatbot.STATE_STATUS[2]
    # else:
        # return sender
    #new_values['$set']['step'] = step + 1

    # return chatbot.update_sender(sender, new_values)
#========== REMOVE ===========#

def ask_credit_details(sender_id, step=0):
    """Return a message according to appropriate number of the credit state
    that bot should send to the user with <sender_id> to collect information.
    """
    text = ""
    quick_reply = []
    # step 0 means it's first time of the user in this state
    if step == 0:
        chatbot.send_message(sender_id, message={'text':'Kredit sifarişi blokuna daxil oldunuz. Zəhmət olmasa, sorğunu doldurun 👇🏻'})
        text = "1/4 : Zəhmət olmasa ad, soyad və ata adını daxil edin daxil edin"
        sender = {'sender_id': sender_id,
                  'step': 0,
                  'state': chatbot.CREDIT_ORDER_STATE,
                  'status': chatbot.STATE_STATUS[0],
                  'start_timestamp': datetime.datetime.now(),
                  'user_data': {}}
        chatbot.insert_sender(sender)
    elif step == 1:
        text = "2/4: Beynəlxalq Bankdan maaş və ya təqaüd kartınız var?"
        quick_reply = chatbot.quick_reply_creator(
            titles=("Bəli", "Xeyr"),
            payloads=(1, 0))
    elif step == 2:
        sender = chatbot.find_sender(sender_id, chatbot.CREDIT_ORDER_STATE)
        if sender['user_data']['is_our_customer']:
            text = "3/4 : Zəhmət olmasa telefon nömrənizi daxil edin 📞"
        else:
            text = "Təəssüf ki, siz Beynəlxalq Bankdan kredit əldə edə bilməzsiniz :( "
            #text = "3/4 : Zəhmət olmasa telefon nömrənizi daxil edin 📞"
        #else:
            #text = "Təəssüf ki, siz Beynəlxalq Bankdan kredit əldə edə bilməzsiniz :( "
        # we can use facebook quick replies object here to get the number.
    elif step == 3:
        sender = chatbot.find_sender(sender_id, chatbot.CREDIT_ORDER_STATE)
        if sender:
            text = "4/4 : Əmək haqqı və ya pensiya kartının 16 rəqəmli nömrəsi"
    else:
        text = "Sizin kredit sorğunuz qeydə alındı, təşəkkürlər. Tezliklə sizə cavab veriləcək. 🙏"
        

    message = {
        'text': text
    }
    if quick_reply:
        message['quick_replies'] = quick_reply

    return message


def save_credit_details(sender, user_message):
    """Return updated <sender> with all information needed to order a credit.
    Store required information included in <user_message> and 
    update number of steps in the database for <sender>.
    """
    step = sender['step']
    new_values = {'$set': {}}

    if step == 0:
        new_values['$set']['user_data.name'] = user_message['text']
    elif step == 1:
        if 'quick_reply' in user_message:
            new_values['$set']['user_data.is_our_customer'] = \
                bool(int(user_message['quick_reply']['payload']))
            #if int(user_message['quick_reply']['payload'])==0:
                #new_values['$set']['status'] = chatbot.STATE_STATUS[1]
                #new_values['$set']['end_timestamp'] = datetime.datetime.now()
    elif step == 2:
        if sender['user_data']['is_our_customer']==1:
            try:
                new_values['$set']['user_data.number'] = int(user_message['text'])
            except ValueError:
                chatbot.send_message(sender['sender_id'], message={
                    'text': 'Zəhmət olmasa, mobil nömrənizi rəqəmlərlə daxil edin, məsələn: 0705505050 '})
                return sender
        else:
            new_values['$set']['status'] = chatbot.STATE_STATUS[1]
            new_values['$set']['end_timestamp'] = datetime.datetime.now()
    elif step == 3:
        if sender['user_data']['is_our_customer'] == 1:
            try:
                new_values['$set']['user_data.card_number'] = int(user_message['text'])
            except ValueError:
                chatbot.send_message(sender['sender_id'], message={
                'text': 'Zəhmət olmasa, 16 rəqəmli kart nömrənizi rəqəmlərlə daxil edin, məsələn: 1111222233334444 '})
                return sender
        # change state status from PENDING to WAITING_APPROVAL
        new_values['$set']['status'] = chatbot.STATE_STATUS[1]
        new_values['$set']['end_timestamp'] = datetime.datetime.now()
    else:
        return sender

    new_values['$set']['step'] = step + 1
    return chatbot.update_sender(sender, new_values)
