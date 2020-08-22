from .parser import parser
from ..control import access, timeout


def handle_auth(update, context, *, command=None,
                function=None, user_id=[]):
    if command == 'list':
        update.message.reply_text(repr(access.show()))

    elif command == 'show':
        update.message.reply_text(repr(access.dir(function)))

    elif command == 'allow':
        for uid in user_id:
            access.allow(function, uid)

    elif command == 'deny':
        for uid in user_id:
            access.deny(function, uid)


def handle_timeout(update, context, *, command=None,
                   function=None, user_id=[]):
    if command == 'list':
        update.message.reply_text(repr(timeout.show()))

    elif command == 'show':
        update.message.reply_text(repr(timeout.dir(function)))

    elif command == 'allow':
        for uid in user_id:
            timeout.allow(function, uid)

    elif command == 'deny':
        for uid in user_id:
            timeout.deny(function, uid)


def handle_list(update, context, *, command=None,
                function=None, user_id=[]):
    pass


def handler(update, context):
    result = parser.parse_args(context.args)

    if hasattr(result, "_message"):
        update.effective_message.reply_html(f"<pre>{result._message}\n</pre>")
        return

    update.effective_message.reply_text(repr(vars(result)))
    dispatch(update, context, **vars(result))


def dispatch(update, context, command=None, subcommand=None, **kwargs):
    handler = {
        'auth': handle_auth,
        'list': handle_list,
        'timeout': handle_timeout,
    }.get(command)

    handler(update, context, command=subcommand, **kwargs)
