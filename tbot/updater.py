import sys
import html

import telegram
import telegram.ext

from functools import wraps
from traceback import format_exception, format_exception_only


class Updater(telegram.ext.Updater):
    def __init__(
        self,
        token=None,
        base_url=None,
        workers=4,
        bot=None,
        private_key=None,
        private_key_password=None,
        user_sig_handler=None,
        request_kwargs=None,
        persistence=None,
        defaults=None,
        dispatcher=None,
        base_file_url=None,
        debug=False,
    ):

        super().__init__(
            token=token,
            base_url=base_url,
            workers=workers,
            bot=bot,
            private_key=private_key,
            private_key_password=private_key_password,
            user_sig_handler=user_sig_handler,
            request_kwargs=request_kwargs,
            persistence=persistence,
            defaults=defaults,
            use_context=True,
            dispatcher=dispatcher,
            base_file_url=base_file_url,
        )

        self.dispatcher.add_error_handler(self.error)

        self.debug = debug

    def error(self, update, context):
        """Log errors back to the chat Errors caused by updates"""
        if not self.debug:
            message = format_exception_only(type(context.error), context.error)

        else:
            message = format_exception(*sys.exc_info())[-8:]

        text = f"<pre>{html.escape(''.join(message))}</pre>"
        context.bot.send_message(
            text=text,
            chat_id=update.effective_chat.id,
            parse_mode=telegram.ParseMode.HTML,
        )

    def command(self, filters=None, command=None):
        def _decorator(decorated):
            self.dispatcher.add_handler(
                telegram.ext.CommandHandler(
                    command if isinstance(command, str) else decorated.__name__,
                    decorated,
                    filters=filters or None,
                )
            )

            @wraps(decorated)
            def _wrap(update, context, *args, **kwargs):
                return decorated(update, context, *args, **kwargs)

            return _wrap

        return _decorator
