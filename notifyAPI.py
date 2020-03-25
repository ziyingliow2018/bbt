# from this link https://www.marcodena.it/blog/telegram-logging-handler-for-python-java-bash/ 
function telegram () {
    curl -s -X POST https://api.telegram.org/bot[Your_API_Key]/sendMessage -d chat_id=[Your_Chat_ID] -d text="$1"}

#!/bin/bash

message=$1
if [[ -n "$message" ]]; then
    curl -s -X POST https://api.telegram.org/bot[Your_API_Key]/sendMessage -d chat_id=[Your_Chat_ID] -d text="$message"
else
    curl -s -X POST https://api.telegram.org/bot[Your_API_Key]/sendMessage -d chat_id=[Your_Chat_ID] -d text="The task is finished."


import requests
from logging import Handler, Formatter
import logging
import datetime

TELEGRAM_TOKEN = 'PUT HERE YOUR TOKENID'
TELEGRAM_CHAT_ID = 'PUT HERE YOUR CHATID'

class RequestsHandler(Handler):
    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': log_entry,
            'parse_mode': 'HTML'
        }
        return requests.post("https://api.telegram.org/bot{token}/sendMessage".format(token=TELEGRAM_TOKEN),
                             data=payload).content

class LogstashFormatter(Formatter):
    def __init__(self):
        super(LogstashFormatter, self).__init__()

    def format(self, record):
        t = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        return "<i>{datetime}</i><pre>\n{message}</pre>".format(message=record.msg, datetime=t)


ogger = logging.getLogger('trymeApp')
logger.setLevel(logging.WARNING)

handler = RequestsHandler()
formatter = LogstashFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.WARNING)

logger.error('We have a problem')




# start here: https://www.codementor.io/@garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay

import json
import requests
import time
import urllib

import config


TOKEN = config.token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()