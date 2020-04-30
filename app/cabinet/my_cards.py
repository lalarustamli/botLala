from app import chatbot
from app.cabinet import my_cards_template

from zeep import Client, Settings
import re
import datetime
import json

import credentials
settings = Settings(strict=False, xml_huge_tree=True)




client = Client(wsdl=credentials.dev_url, settings=settings)


def get_otp(number):
    data = {
            'action': 'chatbot',
            'phoneNumber': number,
    }

    result1 = client.service.getOTPPass(data)
    actual_otp = str(result1['otpPassResult']['otpPass'])
    return actual_otp

def get_fin_phone(fin, phone):
    data = {
        'searchParam': {
            'searchValue':  [fin,phone],
            'searchByType': 'PERSONAL_ID_AND_PHONE',
        },
        'mode': ''
    }
    result = client.service.getCustomerForIBRegistration(data)
    if result['CustomerDetail']!=None:
        customer_num = str(result['CustomerDetail'][0]['base']['customerNumber'])
    else:
        customer_num = None
    return customer_num




def my_cards(personal_id):
    data = {
        'searchParam': {
            'searchByType': 'PERSONAL_ID',
            'searchValue': personal_id,
        },
        'mode': 'card'
    }
    result1 = str(client.service.getCustomerDetails(data))
    # result2 = str(client.service.getCurrencyRates())
    stri = result1.replace("\'", "\"")
    stri2 = re.sub("Decimal( |)", "", stri)
    stri3 = stri2.replace("(", "")
    stri4 = stri3.replace(")", "")
    result = eval(stri4)

    card_info = []
    # print("result 2: "+ result2)
    if result['CustomerDetail']:
        card_list=result['CustomerDetail'][0]['cards']['card']
        for card in card_list:
            cardName = card['cardName']
            cardNumber = card['cardNumber']
            availableBalance = card['availableBalance']
            card_necessary_info={
            'cardName':str(cardName),
            'cardNumber': cardNumber,
            'availableBalance': str(availableBalance)
        }
            card_info.append(card_necessary_info)
    return card_info

def ask_card_info(sender_id, step=0):
    text = ""
    quick_reply = []

    if step == 0:
        text = "Şəxsiyyət vəsiqənizdəki FİN kodu daxil edin"

        sender = {'sender_id': sender_id,
                  'step': 0,
                  'state': chatbot.MY_CARDS_STATE,
                  'status': chatbot.STATE_STATUS[0],
                  'start_timestamp': datetime.datetime.now(),
                  'user_data': {}}
        chatbot.insert_sender(sender)
    elif step == 1:
        text = "Mobil telefon nömrənizi daxil edin. Məsələn, 994503101010"
    elif step == 2:
        text = "OTP kodu daxil edin"
    else:
        new_values = {'$set': {}}
        sender = chatbot.find_sender(sender_id, chatbot.MY_CARDS_STATE)
        new_values['$set']['status'] = chatbot.STATE_STATUS[2]
        chatbot.update_sender(sender, new_values)
        if sender['user_data']['personal_id']:
            if sender['user_data']['fin_phone']:
                if sender['user_data']['recorded_otp']==sender['user_data']['real_otp']:
                    personal_id=sender['user_data']['personal_id']
                    card_info = my_cards(personal_id)
                    if len(card_info)==0:
                        chatbot.send_message(sender_id, message={'text': 'Xəta baş verdi. Daxil etdiyiniz FİN-ə uyğun kart tapılmadı.'})
                    else:
                        message=my_cards_template.my_cards_menu(sender_id,card_info)
                        chatbot.send_message(sender_id,message)
                else:
                    chatbot.send_message(sender_id, message={'text': "OTP tapilmadi"})
            else:
                chatbot.send_message(sender_id, message={'text': "Telefon nömrənizlə fin kod uyğun gəlmir"})
        else:
            text = "Tapılmadı."

    message = {
        'text': text
    }

    return message


def save_my_cards_state(sender, user_message):
    """Return updated <sender>. Store <sender> information from <user_message>
    and update step number in the database.
    """
    step = sender['step']
    new_values = {'$set': {}}

    if step == 0:
        if len(str(user_message['text']))==7:
            new_values['$set']['user_data.personal_id'] = str(user_message['text']).upper()
        else:
            chatbot.send_message(sender['sender_id'], message={
                'text': '7 rəqəmli FİN kodu daxil edin'})
            chatbot.clear_sender_state(sender['sender_id'])
            return sender
    elif step == 1:
        if len(str(user_message['text']))==12:
            new_values['$set']['user_data.number'] = int(user_message['text'])
            new_values['$set']['user_data.fin_fon_number'] = str(user_message['text']).replace('994','0')
            new_values['$set']['user_data.fin_phone'] = get_fin_phone(sender['user_data']['personal_id'],str(user_message['text']).replace('994','0'))
            new_values['$set']['user_data.real_otp'] = get_otp(int(user_message['text']))
        else:
            chatbot.send_message(sender['sender_id'], message={
                'text': 'Zəhmət olmasa, telefon nömrənizi 12 rəqəmli şəkildə daxil edin, məsələn, 994503101010'})
            return sender
    elif step ==2:
        new_values['$set']['user_data.recorded_otp'] =str(user_message['text'])

    else:
        return sender
    new_values['$set']['step'] = step + 1
    return chatbot.update_sender(sender, new_values)


def card_to_card(debit,debitor,credit,creditor,currency,amount):
    data = {
        'debit': {
            'cardNumber': str(debit),
            'cardHolderName': str(debitor),
        },
        'credit': {
            'cardNumber': 'N'+str(credit),
            'cardHolderName': str(creditor),
        },
        'currency': str(currency),
        'amount':str(amount)
    }
    result = client.service.setCardToCardPayment(data)
    result2=result['status']['errorCode']
    return result2





def ask_card_to_card_info(sender_id,step=0):
    text = ""
    quick_reply = []
    if step == 0 or step==1:
        text = "Göndərmək istədiyiniz kart nömrəsini daxil edin"
    elif step == 2:
        text = "Kart sahibini daxil edin"
    elif step == 3:
        print('step1')
        text = "Məzənnəni seçin"
        quick_reply = chatbot.quick_reply_creator(titles=("USD", "AZN", "EUR"),
                                                  payloads=('USD', 'AZN', 'EUR'))
    elif step== 4:
        text="Məbləği daxil edin"
    else:
        new_values = {'$set': {}}
        sender = chatbot.find_sender(sender_id, chatbot.CARD_TO_CARD_STATE)
        new_values['$set']['status'] = chatbot.STATE_STATUS[2]
        chatbot.update_sender(sender, new_values)
        if sender['user_data']['credit_number']:
            debit=sender['user_data']['debit_number']
            debitor=sender['user_data']['debit_name']
            currency=sender['user_data']['card_to_card_currency']
            amount = sender['user_data']['card_to_card_amount']
            message=card_to_card(debit,debitor,sender['user_data']['credit_number'],sender['user_data']['credit_name'],currency,amount)
            if message==None:
                chatbot.send_message(sender_id,message={'text':'Ödəniş uğurla başa çatdı'})
            else:
                chatbot.send_message(sender_id, message={'text': 'Xəta baş verdi'})
        else:
            text='16 rəqəmli kart nömrəsi yalnış daxil edilib'
    message = {
        'text': text
    }
    if quick_reply:
        message['quick_replies'] = quick_reply

    return message

def save_card_to_card_state(sender, user_message):
    """Return updated <sender>. Store <sender> information from <user_message>
    and update step number in the database.
    """
    step = sender['step']
    new_values = {'$set': {}}

    if step == 1:
        if len(str(user_message['text']))==16:
            new_values['$set']['user_data.credit_number'] = str(user_message['text'])
        else:
            chatbot.send_message(sender['sender_id'], message={
                'text': '16 rəqəmli kart nömrəsini daxil edin'})
            print(sender)
            return sender
    elif step ==2:
        if user_message:
            new_values['$set']['user_data.credit_name'] = str(user_message['text'])
        else:
            return sender
    elif step == 3:
        if 'quick_reply' in user_message:
            new_values['$set']['user_data.card_to_card_currency'] = str(
                user_message['quick_reply']['payload'])
        elif 'text' in user_message:
            if user_message['text'] =='AZN' or user_message['text'] =='USD' or user_message['text'] =='EUR':
                new_values['$set']['user_data.card_to_card_currency']=user_message['text']
            else:
                chatbot.send_message(sender['sender_id'],
                                     message={'text': 'Zəhmət olmasa, mövcud seçimlərdən birini edin'})
                chatbot.clear_sender_state(sender['sender_id'])
                return sender
        else:
            chatbot.send_message(sender['sender_id'],
                                 message={'text': 'Zəhmət olmasa, mövcud seçimlərdən birini edin'})
            chatbot.clear_sender_state(sender['sender_id'])
            return sender
    elif step==4:
        if user_message:
            new_values['$set']['user_data.card_to_card_amount'] = str(user_message['text'])
        else:
            return sender

    else:
        return sender

    new_values['$set']['step'] = step + 1
    return chatbot.update_sender(sender, new_values)


