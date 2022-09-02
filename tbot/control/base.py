# no need for singleton as modules are imported only once
class Singleton(type):
    """https://stackoverflow.com/a/6798042"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseDecorator:
    def __init__(self):
        self._context = {}

    def __getitem__(self, function):
        if isinstance(function, str):
            function = dict(zip(dir(self), self)).get(function)

        return self._context[function]

    def __iter__(self):
        return iter(self._context)

    def __dir__(self):
        return [f.__name__ for f in self]
