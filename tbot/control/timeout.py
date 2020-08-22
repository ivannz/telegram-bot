from datetime import datetime, timedelta

from telegram.error import TelegramError

from functools import wraps

from .base import BaseDecorator


class TimeOutError(TelegramError):
    pass


class TimeOutDecorator(BaseDecorator):
    def allow(self, function, user_id):
        self[function].pop(user_id, None)

    def deny(self, function, user_id):
        self[function][user_id] = datetime.fromisoformat('5999-12-31 23:59:59')

    @wraps(timedelta)
    def apply(self, *, ontimeout='ignore', **timeout):
        assert ontimeout in ('ignore', 'refresh')
        timeout = timedelta(**timeout)
        if timeout.total_seconds() <= 0:
            raise TypeError(f"`timeout` must be positive. Got `{timeout}`.")

        def _decorator(decorated):
            self._context.setdefault(decorated, {})

            @wraps(decorated)
            def _wrap(update, context, *args, **kwargs):
                timeouts, curr = self._context[decorated], datetime.now()

                prev = timeouts.get(update.effective_user.id, curr - timeout)
                remaining = timeout - (curr - prev)
                try:
                    if remaining.total_seconds() > 0:
                        raise TimeOutError(
                            f'`{update.effective_user.username}` is timed '
                            f'out for {remaining}.')

                    return decorated(update, context, *args, **kwargs)

                finally:
                    if remaining.total_seconds() <= 0 or ontimeout == 'refresh':
                        timeouts[update.effective_user.id] = curr

            return _wrap

        return _decorator

    def __call__(self, *authorized):
        return self.apply(*authorized)


_instance = TimeOutDecorator()

apply, allow, deny = _instance.apply, _instance.allow, _instance.deny


def show():
    return {fn.__name__: _instance[fn] for fn in _instance}


def dir(function):
    return _instance[function]
