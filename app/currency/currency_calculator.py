import requests
import datetime
import pytz
import xml.etree.ElementTree as ET
from pymongo import MongoClient


def get_currencies_from_cbar():
    """Return today currency as a dictionary where keys are valute code
    and values are rates such as 'USD': '1.7'.
    """
    
    # get current date and time for baku/azerbaijan
    baku_timezone = pytz.country_timezones('AZ')[0]
    baku_dt = datetime.datetime.now(pytz.timezone(baku_timezone))
    
    current_date = baku_dt.strftime("%d.%m.%Y")
    
    current_time = baku_dt.strftime("%H:%M")
    
    
    

    #client = MongoClient("mongodb://ibar:ibar2019@ibarchatbot-shard-00-00-2pyzh.mongodb.net:27017,ibarchatbot-shard-00-01-2pyzh.mongodb.net:27017,ibarchatbot-shard-00-02-2pyzh.mongodb.net:27017/test?ssl=true&replicaSet=ibarchatbot-shard-0&authSource=admin&retryWrites=true")
    #db = client['chatbotdb']
    #config = db['config']
    #last_cbar_request = config.find_one(
        #{'name': 'currency'})
    #client.close()


    # check whether we have already stored today rates
    # if not, make request to CBAR and update cbar_currency_list file
    if (current_date != last_cbar_request['last_date'] and '09:45' < current_time < '10:15'):
        update_cbar_currencies_file()

    result = {}
    try:
        tree = ET.parse('files/cbar_currency_list.xml')
        root = tree.getroot()
        valtypes = root.findall('ValType/[@Type="Xarici valyutalar"]/Valute')
        for t in valtypes:
            result[t.attrib['Code']] = float(t.find('Value').text)
    except:
        raise Exception('no such file exists.')

    return result

def update_cbar_currencies_file():
    url = "https://www.cbar.az/currencies/" + current_date + ".xml"
    response = requests.get(url)
    
    with open('files/cbar_currency_list.xml', 'wb') as currencies:
        currencies.write(response.content)
    
    currencies.close()