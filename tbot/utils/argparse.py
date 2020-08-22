import io
import sys

from contextlib import redirect_stdout, redirect_stderr

from argparse import ArgumentParser as BaseArgumentParser
from argparse import ArgumentError, Namespace


class ArgumentParser(BaseArgumentParser):
    def error(self, message):
        # in the original `.error` method `stderr` contains usage
        type, value, traceback = sys.exc_info()
        if type is not None:
            # reraise if `.error` was called from a try-except clause
            raise

        # do not call `.exit` on `.error`
        raise ArgumentError(None, message)

    def parse_known_args(self, args, namespace=None):
        with io.StringIO() as stdout, io.StringIO() as stderr, \
           redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                # Redirect the stdout/stderr to string buffers
                # with redirect_stdout(stdout), redirect_stderr(stderr):
                return super().parse_known_args(
                    args=args, namespace=namespace)

            except SystemExit:
                return Namespace(_message=stdout.getvalue()), []

    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        if argv:
            raise ArgumentError(None, f'Unrecognized arguments {argv}')
        return args
