""" pywit is the Python SDK for Wit.ai.
 Provides a <Wit> class with <message> , <speech> and <interactive> methods. For more information visit : https://github.com/wit-ai/pywit
 """
import credentials as cr
from wit import Wit
access_token = cr.WIT_TOKEN
client = Wit(access_token=access_token)

def wit_response(user_message):
    """ Return Wit.ai <entity> and <value> of message based on <user_message>
    """
    resp = client.message(user_message)
    entity = None
    value = None

    try:
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
    except:
        pass
    return (entity, value)
