import os

import telegram
from telegram.ext import Filters, MessageHandler

from . import admin
from .updater import Updater
from .control import access, timeout, logging


# logging.basicConfig(
#     filename='report.log', style='{',
#     format='{asctime:24} {levelname:12} {name} {message}',
#     level=logging.INFO)

# logger = logging.getLogger(__name__)


# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Storing-bot,-user-and-chat-related-data
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#requesting-location-and-contact-from-user

updater = Updater(os.environ.get('TOKEN') or open('.token').read().strip())


@updater.command(command='iddqd')
@access.apply(191745228)
def admin_handler(update, context):
    return admin.handler(update, context)


# @log.apply
@timeout.apply(seconds=10)
@access.apply()
def echo(update, context):
    update.message.reply_text(update.message.text)


updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()
updater.idle()
