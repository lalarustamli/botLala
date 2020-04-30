from app import chatbot
import requests
import datetime
import xml.etree.ElementTree as ET
from pymongo import MongoClient


def get_iba_rates(base, quote):
    """Returns foreign exchange rates based on api (global)
    """
    API_KEY = 'd7145b955df4089db505'
    url = 'https://free.currencyconverterapi.com/api/v6/convert?q=' + \
        base + '_' + quote + '&compact=ultra&apiKey=' + API_KEY
    response = requests.get(url)
    data = response.json()
    for_ex = float(data[base + '_' + quote])
    return for_ex


def iba_currency_calculator(base, quote, amount):
    """Return converted value of <amount> from <base> currency to <quote> currency
    according to foreign exchange rates requested from global api.
    """
    return round(amount * get_iba_rates(base, quote),2)


def ask_iba_currency_calculator_details(sender_id, step=0):
    """Return a message according to appropriate number of the IBA currency 
    calculator state that bot should send to the user with <sender_id> 
    to collect information.
    """
    text = ""
    quick_reply = []

    if step == 0:
        text = "Hansı məzənnəyə əsasən hesablamaq istəyirsiniz?"
        quick_reply = chatbot.quick_reply_creator(titles=("USD", "AZN", "EUR"),
                                                  payloads=('USD', 'AZN', 'EUR'))
        sender = {'sender_id': sender_id,
                  'step': 0,
                  'state': chatbot.CURRENCY_STATE[0],
                  'status': chatbot.STATE_STATUS[0],
                  'start_timestamp': datetime.datetime.now(),
                  'user_data': {}}
        chatbot.insert_sender(sender)
    elif step == 1:
        text = "Hansı məzənnəyə çevirmək istəyirsiniz?"
        quick_reply = chatbot.quick_reply_creator(titles=("USD", "AZN", "EUR"),
                                                  payloads=('USD', 'AZN', 'EUR'))
    elif step == 2:
        text = "Məbləği daxil edin"
    else:
        new_values = {'$set': {}}
        sender = chatbot.find_sender(sender_id, chatbot.CURRENCY_STATE[0])
        new_values['$set']['status'] = chatbot.STATE_STATUS[2]
        chatbot.update_sender(sender, new_values)

        final_amount = iba_currency_calculator(sender['user_data']['base'],
                                               sender['user_data']['quote'],
                                               sender['user_data']['amount'])
        # (ex): 100 USD = 169.70 AZN
        text = "{} {} = {} {}".format(sender['user_data']['amount'],
                                      sender['user_data']['base'],
                                      final_amount,
                                      sender['user_data']['quote'])

    message = {
        'text': text
    }

    if quick_reply:
        message['quick_replies'] = quick_reply

    return message


def save_iba_currency_calculator(sender, user_message):
    """Return updated with all information needed for an IBA currency 
    calculator. Store required information included in <user_message> and 
    update number of steps in the database for.
    """
    step = sender['step']
    new_values = {'$set': {}}

    if step == 0:
        if 'quick_reply' in user_message:
            new_values['$set']['user_data.base'] = str(
                user_message['quick_reply']['payload'])
        else:
            # !!!!!!!!!! check if user enters it manually
            chatbot.send_message(sender['sender_id'],
                                 message={'text': 'Zəhmət olmasa, mövcud seçimlərdən birini edin'})
            chatbot.clear_sender_state(sender['sender_id'])
            return sender
    elif step == 1:
        if 'quick_reply' in user_message:
            new_values['$set']['user_data.quote'] = str(
                user_message['quick_reply']['payload'])
    elif step == 2:
        new_values['$set']['user_data.amount'] = float(user_message['text'])

        new_values['$set']['user_data.rate'] = get_iba_rates(sender['user_data']['base'],
                                                             sender['user_data']['quote'])
        new_values['$set']['user_data.converted_amount'] = \
            iba_currency_calculator(sender['user_data']['base'],
                                    sender['user_data']['quote'],
                                    float(user_message['text']))

        new_values['$set']['end_timestamp'] = datetime.datetime.now()
    else:
        return sender

    new_values['$set']['step'] = step + 1
    return chatbot.update_sender(sender, new_values)


def get_currencies_from_cbar(sender_id):
    """Return today currency as a dictionary where keys are valute code
    and values are rates such as 'USD': '1.7'.
    """
    sender = {'sender_id': sender_id,
              'state': chatbot.CURRENCY_STATE[2],
              'status': chatbot.STATE_STATUS[2],
              'start_timestamp': datetime.datetime.now(),
              'user_data': {}}
    chatbot.insert_sender(sender)
    current_date = datetime.date.today().strftime("%d.%m.%Y")
    client = MongoClient(chatbot.DB_URL)
    db = client['chatbotdb']
    config = db['config']
    last_cbar_request = config.find_one(
        {'name': 'currency'})
    client.close()

    # check whether we have already stored today rates
    # if not, make request to CBAR and update cbar_currency_list file
    if (current_date != last_cbar_request['last_date']):
        url = "https://www.cbar.az/currencies/" + current_date + ".xml"
        response = requests.get(url)

        with open('/var/www/chatbot/files/cbar_currency_list.xml', 'wb') as currencies:
            currencies.write(response.content)

        config.find_one_and_update(
            last_cbar_request, {'$set': {'last_date': current_date}})
        currencies.close()
    result = {}
    try:
        tree = ET.parse('/var/www/chatbot/files/cbar_currency_list.xml')
        root = tree.getroot()
        valtypes = root.findall('ValType/[@Type="Xarici valyutalar"]/Valute')
        for t in valtypes:
            result[t.attrib['Code']] = float(t.find('Value').text)
    except:
        raise Exception('no such file exists.')

    message = {
        'text': ' 🏦 Mərkəzi Bank valyuta məzənnələri:'
                '\n 🇺🇸 1 USD : ' + str(result['USD']) + ' AZN' +
                '\n 🇪🇺 1 EUR : ' + str(result['EUR']) + ' AZN' +
                '\n 🇷🇺 1 RUB : ' + str(result['RUB']) + ' AZN' +
                '\n 🇹🇷 1 TRY : ' + str(result['TRY']) + ' AZN' +
                '\n 🇬🇪 1 GEL : ' + str(result['GEL']) + ' AZN' +
                '\n 🇬🇧 1 GBP : ' + str(result['GBP']) + ' AZN'
    }

    return message
