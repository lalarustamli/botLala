import requests
from enum import Enum
from app import chatbot
from pymongo import MongoClient, ReturnDocument

API = "https://graph.facebook.com/v5.0/me/messages"
RECIPIENT_FIELD = "recipient"
MESSAGE_FIELD = "message"
NOTIFICATION_FIELD = "notification_type"
TYPE_FIELD = "type"
PAYLOAD_FIELD = "payload"
TITLE_FIELD = "title"
URL_FIELD = "url"
CONTENT_FIELD = "content_type"
QUICK_REPLY_FIELD = "quick_replies"
ATTACHMENT_FIELD = "attachment"
TEMPLATE_TYPE_FIELD = "template_type"
BUTTONS_FIELD = "buttons"
ELEMENTS_FIELD = "elements"
SUBTITLE_FIELD = "subtitle"
IMAGE_FIELD = "image_url"


class Recipient(Enum):
    PHONE_NUMBER = "user_phone_number"
    EMAIL = "user_email"
    ID = 'id'


class NotificationType(Enum):
    regular = "REGULAR"
    silent_push = "SILENT_PUSH"
    no_push = "NO_PUSH"


class MessageType(Enum):
    TEXT = "text"
    ATTACHMENT = "attachment"


class AttachmentType(Enum):
    IMAGE = "image"
    TEMPLATE = "template"


class TemplateType(Enum):
    GENERIC = "generic"
    BUTTON = "button"
    RECEIPT = "receipt"


class ButtonType(Enum):
    WEB_URL = "web_url"
    POSTBACK = "postback"


class ButtonList:

    def __init__(self, button_types, titles, urls=None, payloads=None):
        self.button_types = button_types
        self.titles = titles
        self.urls = urls
        self.payloads = payloads

    def btn_list(self):
        btn_l = []
        for button_type, title, url, payload in zip(self.button_types, self.titles, self.urls, self.payloads):
            btn_l.append({
                TYPE_FIELD: button_type,
                TITLE_FIELD: title,
                URL_FIELD: url,
                PAYLOAD_FIELD: payload
            })
        return btn_l


class QuickReply():

    def __init__(self, titles, payloads):
        self.titles = titles
        self.payloads = payloads
        self.image_url = None

    def text_quick_reply_creator(self):
        quick_reply = []
        for title, payload in zip(self.titles, self.payloads):
            quick_reply.append({
                CONTENT_FIELD: MessageType.TEXT.value,
                TITLE_FIELD: title,
                PAYLOAD_FIELD: payload
            })

        return self.quick_reply

    def phone_quick_reply(self):
        self.quick_reply.append({
            CONTENT_FIELD: Recipient.PHONE_NUMBER.value
            # PAYLOAD_FIELD: payload
        })
        return self.quick_reply

    def email_quick_reply(self):
        self.quick_reply.append({
            CONTENT_FIELD: Recipient.EMAIL.value
        })
        return self.quick_reply


class GenericElement:
    def __init__(self, title, subtitle, image_url, buttons):
        self.title = title
        self.subtitle = subtitle
        self.image_url = image_url
        self.buttons = buttons

    def to_dict(self):
        element_dict = {BUTTONS_FIELD: [
            button.to_dict() for button in self.buttons]}
        if self.title:
            element_dict[TITLE_FIELD] = self.title
        if self.subtitle:
            element_dict[SUBTITLE_FIELD] = self.subtitle
        if self.image_url:
            element_dict[IMAGE_FIELD] = self.image_url
        return element_dict

class Bot:
    def __init__(self, token):
        self.token = token

    def __send(self, message_data):
        payload = message_data
        auth = {
            'access_token': self.token
        }
        response = requests.post(
            API,
            params=auth,
            json=payload
        )
        print('payload1' + str(payload))
        return response.json()

    def send_message(self, recipient_id, text):
        """Send a response to Facebook by making a post request.
            """
        payload = {
            MESSAGE_FIELD: {MessageType.TEXT.value: text},
            RECIPIENT_FIELD: self._build_recipient(recipient_id),
            NOTIFICATION_FIELD: NotificationType.regular.value
        }
        self.__send(payload)

    def send_image(self, recipient_id, url):
        image = {
            TYPE_FIELD: AttachmentType.IMAGE.value,
            PAYLOAD_FIELD: {
                URL_FIELD: url,
                'is_reusable': 'True'
            }
        }
        payload = {
            MESSAGE_FIELD: {MessageType.ATTACHMENT.value: image},
            RECIPIENT_FIELD: self._build_recipient(recipient_id),
            NOTIFICATION_FIELD: NotificationType.regular.value
        }
        self.__send(payload)

    def quick_reply(self, recipient_id, text, titles, payloads):
        quick_reply = QuickReply(titles, payloads).text_quick_reply_creator()
        message = {
            MESSAGE_FIELD: {
                MessageType.TEXT.value: text,
                QUICK_REPLY_FIELD: quick_reply
            },
            RECIPIENT_FIELD: self._build_recipient(recipient_id),
            NOTIFICATION_FIELD: NotificationType.regular.value
        }
        self.__send(message)


    def phone_number_quick_reply(self, recipient_id, text):
        quick_reply = QuickReply(titles=None, payloads=None).phone_quick_reply()
        message = {
            MESSAGE_FIELD: {
                MessageType.TEXT.value: text,
                QUICK_REPLY_FIELD: quick_reply
            },
            RECIPIENT_FIELD: self._build_recipient(recipient_id),
            NOTIFICATION_FIELD: NotificationType.regular.value
        }
        self.__send(message)

    def email_quick_reply(self, recipient_id, text):
        quick_reply = QuickReply(titles=None, payloads=None).email_quick_reply()
        message = {
            MESSAGE_FIELD: {
                MessageType.TEXT.value: text,
                QUICK_REPLY_FIELD: quick_reply
            },
            RECIPIENT_FIELD: self._build_recipient(recipient_id),
            NOTIFICATION_FIELD: NotificationType.regular.value
        }
        self.__send(message)

    def send_button_template(self, recipient_id, text, types, titles, urls, payloads):
        button_list = ButtonList(types, titles, urls, payloads).btn_list()
        payload = {
            MESSAGE_FIELD: {
                ATTACHMENT_FIELD: {
                    TYPE_FIELD: AttachmentType.TEMPLATE.value,
                    PAYLOAD_FIELD: {
                        TEMPLATE_TYPE_FIELD: TemplateType.BUTTON.value,
                        MessageType.TEXT.value: text,
                        BUTTONS_FIELD: button_list
                    }
                },
            },
            RECIPIENT_FIELD: self._build_recipient(recipient_id),
            NOTIFICATION_FIELD: NotificationType.regular.value
        }
        self.__send(payload)

    def send_generic_template(self, recipient_id, elements):
        # elems = [element.to_dict() for element in elements]
        payload = {
                MESSAGE_FIELD: {
                    ATTACHMENT_FIELD: {
                        TYPE_FIELD: AttachmentType.TEMPLATE.value,
                        PAYLOAD_FIELD: {
                            TEMPLATE_TYPE_FIELD: TemplateType.GENERIC.value,
                            'image_aspect_ratio': 'horizontal',
                            ELEMENTS_FIELD: elements
                        }
                    }
                },
                RECIPIENT_FIELD: self._build_recipient(recipient_id),
                NOTIFICATION_FIELD: NotificationType.regular.value
            }
        self.__send(payload)

    @staticmethod
    def _build_recipient(recipient_id):
        return {Recipient.ID.value: recipient_id}


class MongoDB():
    def __init__(self):
        self.client = MongoClient(chatbot.DB_URL)
        self.db = self.client['chatbotdb']
        self.user_states = self.db['user_states']

    def find_sender(self, sender_id, state, status):
        sender_to_find = self.user_states.find_one({'sender_id': sender_id, 'state': state, 'status': status})
        self.client.close()
        return sender_to_find

    def insert_sender(self, sender):
        self.user_states.insert_one(sender)
        self.client.close()

    def update_sender(self, new_values, sender):
        updated_sender = self.user_states.find_one_and_update(
            sender, new_values, return_document=ReturnDocument.AFTER)
        self.client.close()
        return updated_sender

    def sender_has_state(self, sender_id):
        sender = self.user_states.find_one(
            {'sender_id': sender_id, 'status': chatbot.STATE_STATUS[0]})
        self.client.close()
        if sender:
            return True, sender
        return False, None

    def clear_sender_state(self, sender_id):
        self.user_states.delete_one(
            {'sender_id': sender_id, 'status': chatbot.STATE_STATUS[0]})
        self.client.close()
