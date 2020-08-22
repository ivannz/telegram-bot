from datetime import datetime
from functools import wraps

from .base import BaseDecorator


class LoggingDecorator(BaseDecorator):
    def apply(self, decorated):
        """Decorator for tracking function calls."""
        self._context.setdefault(decorated, {})

        @wraps(decorated)
        def _wrap(update, context, *args, **kwargs):
            info = datetime.now(), update.effective_user.username
            try:
                return decorated(update, context, *args, **kwargs)

            finally:
                self._context[decorated][update.effective_user.id] = info

        return _wrap

    def __call__(self):
        return self.apply()


_instance = LoggingDecorator()

apply = _instance.apply


def show():
    return {fn.__name__: _instance[fn] for fn in _instance}
