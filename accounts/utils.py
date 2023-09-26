import requests
from datetime import datetime
from django.utils.crypto import get_random_string



BASE_URL = 'http://api.smsgw.net/'

def services_alive():
    try:
        response = requests.get('{}{}'.format(BASE_URL, "IsServiceAlive"))
        return response.json()
    except Exception as e:
        print(e)
        return False


def list_to_string(orginal_list,delim):
    res = ''
    for ele in orginal_list:
        res = res + str(ele) + delim
    return str(res)


def SendBulkSMS(strMessage, recepientNumbers):
    try:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %I:%M %p")
        strRecepientNumbers = list_to_string(recepientNumbers, ',')

        post_data = {'strUserName':'9665xxxxxxx','strPassword':'','strTagName':'SMSgw.net',
                 'strRecepientNumbers':strRecepientNumbers,'strMessage':strMessage,
                 'sendDateTime':'%Y-%m-%d %I:%M %p {}'.format(dt_string),}
        response = requests.post("{}{}".format(BASE_URL, "SendBulkSMS"), post_data)
        return response.json()
    except Exception as e:
        print("error at SendBlukSms", e)
        return False

def SendInternationalSMS(strMessage, recepientNumbers):
    try:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %I:%M %p")
        strRecepientNumbers = list_to_string(recepientNumbers, ',')

        post_data = {'strUserName':'9665xxxxxxx','strPassword':'','strTagName':'SMSgw.net',
                 'strRecepientNumbers':strRecepientNumbers,'strMessage':strMessage,
                 'sendDateTime':'%Y-%m-%d %I:%M %p {}'.format(dt_string),}
        response = requests.post("{}{}".format(BASE_URL, "SendInternationalSMS"), post_data)
        return response.json()
    except Exception as e:
        print("Error At SendInternationalSMS",e)
        return False


def SendSingleSMS(strMessage, recepientNumber):
    try:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %I:%M %p")

        post_data = {'strUserName':'9665xxxxxxx','strPassword':'','strTagName':'SMSgw.net',
                 'strRecepientNumbers':recepientNumber,'strMessage':strMessage,
                 'sendDateTime':'%Y-%m-%d %I:%M %p {}'.format(dt_string),}
        response = requests.post("{}{}".format(BASE_URL, "SendSingleSMS"), post_data)
        return response.json()
    except Exception as e:
        print("Error At SendSingleSMS",e)
        return False


def generate_digits():
    number = get_random_string(length=6, allowed_chars='1234567890')
    return number