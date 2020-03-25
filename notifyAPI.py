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