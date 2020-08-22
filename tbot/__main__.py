import sys
import html

from functools import wraps

from traceback import format_exception

from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler

from .control import access, timeout, logging
from . import admin


# logging.basicConfig(
#     filename='report.log', style='{',
#     format='{asctime:24} {levelname:12} {name} {message}',
#     level=logging.INFO)

# logger = logging.getLogger(__name__)


updater = Updater(open('.token', 'rt').read().strip(), use_context=True)


@updater.dispatcher.add_error_handler
def error(update, context, debug=False):
    """Log errors back to the chat Errors caused by updates"""
    if not debug:
        e = context.error
        update.effective_message.reply_text(f"{type(e).__name__}, {str(e)}")
        return

    traceback = html.escape(''.join(format_exception(*sys.exc_info())[-10:]))
    update.effective_message.reply_html(f"<pre>{traceback}</pre>")


def register(*, filters, command=None):
    global updater
    dp = updater.dispatcher

    def _decorator(decorated):
        cmd = decorated.__name__ if not isinstance(command, str) else command
        dp.add_handler(CommandHandler(cmd, decorated, filters=filters))

        @wraps(decorated)
        def _wrap(update, context, *args, **kwargs):
            return decorated(update, context, *args, **kwargs)

        return _wrap

    return _decorator


@register(filters=None, command='iddqd')
@access.apply(191745228)
def admin_handler(update, context):
    return admin.handler(update, context)


# @log.apply
@access.apply()
@timeout.apply(seconds=10)
def echo(update, context):
    update.message.reply_text(update.message.text)


updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()
updater.idle()
