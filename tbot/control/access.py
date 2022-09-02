from functools import wraps
from telegram.error import Unauthorized

from .base import BaseDecorator


class UnauthorizedError(Unauthorized):
    pass


class AccessDecorator(BaseDecorator):
    def allow(self, function, user_id):
        self[function].add(user_id)

    def deny(self, function, user_id):
        self[function].remove(user_id)

    def apply(self, *authorized):
        """Decorator for restricting function calls."""

        def _decorator(decorated):
            self._context.setdefault(decorated, set(authorized))

            @wraps(decorated)
            def _wrap(update, context, *args, **kwargs):
                authorized = self._context[decorated]
                if update.effective_user.id not in authorized:
                    username = update.effective_user.username
                    function = decorated.__name__
                    raise UnauthorizedError(f"`{username}` cannot use `{function}`")

                return decorated(update, context, *args, **kwargs)

            return _wrap

        # replace the `decorator` with `_decorator` (saving frame),
        #  which after being called is substituted by `_wrap`.
        return _decorator

    def __call__(self, *authorized):
        return self.apply(*authorized)


_instance = AccessDecorator()

apply, allow, deny = _instance.apply, _instance.allow, _instance.deny


def show():
    return {fn.__name__: _instance[fn] for fn in _instance}


def dir(function):
    return _instance[function]
