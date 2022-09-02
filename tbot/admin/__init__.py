from .parser import parser
from ..control import access, timeout


def handle_auth(context, command=None, function=None, user_id=[]):
    if command == "list":
        return repr(access.show())

    elif command == "show":
        return repr(access.dir(function))

    elif command == "allow":
        for uid in user_id:
            access.allow(function, uid)

    elif command == "deny":
        for uid in user_id:
            access.deny(function, uid)


def handle_timeout(context, command=None, function=None, user_id=[]):
    if command == "list":
        return repr(timeout.show())

    elif command == "show":
        return repr(timeout.dir(function))

    elif command == "allow":
        for uid in user_id:
            timeout.allow(function, uid)

    elif command == "deny":
        for uid in user_id:
            timeout.deny(function, uid)


def handle_list(context, command=None, function=None, user_id=[]):
    return ""


def handler(update, context):
    def dispatch(service=None, **kwargs):
        handler = {
            "auth": handle_auth,
            "list": handle_list,
            "timeout": handle_timeout,
        }.get(service)

        return handler(context, **kwargs)

    result = parser.parse_args(context.args)

    if hasattr(result, "_message"):
        update.effective_message.reply_html(f"<pre>{result._message}\n</pre>")
        return

    update.effective_message.reply_text(repr(vars(result)))
    update.effective_message.reply_text(dispatch(**vars(result)))
