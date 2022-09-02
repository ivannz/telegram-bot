from argparse import ArgumentTypeError
from ..utils.argparse import ArgumentParser


def identifier(object):
    """Check if the argument is a valid identifier."""
    if object.isidentifier():
        return object

    raise ArgumentTypeError(f"`{object}` is not a valid indentifier.")


function = ArgumentParser(add_help=False)
function.add_argument(
    "function", type=identifier, help="The name of the function to allow / deny access."
)

user_id = ArgumentParser(add_help=False)
user_id.add_argument("user_id", type=int, nargs="+", help="A list of integer user ids.")

# main admin control parser
parser = ArgumentParser(
    prog="admin",
    description="Telegram bot admin.",
    epilog="""Three shalt be the number thou shalt count, and the number """
    """of the counting shall be three. Four shalt thou not count, """
    """nor either count thou two, excepting that thou then proceed """
    """to three.""",
)
subparsers = parser.add_subparsers(dest="service", required=True)


# User information
subparser = subparsers.add_parser(
    "list", aliases=["ls"], help="Show tracked access requests."
)


# User information and access
subparser = subparsers.add_parser("auth", help="Manage access rights.")

subsubparsers = subparser.add_subparsers(dest="command")

subsubparser = subsubparsers.add_parser(
    "allow", parents=[function, user_id], help="Authorize a new user."
)

subsubparser = subsubparsers.add_parser(
    "deny", parents=[function, user_id], help="Deauthorize an existing user."
)

subsubparser = subsubparsers.add_parser(
    "show", parents=[function], help="Show the list of authorized users."
)

subsubparser = subsubparsers.add_parser(
    "list", parents=[], help="Show the list of registered functions."
)

# Timeout management
subparser = subparsers.add_parser(
    "timeout", aliases=["to"], help="Manage timeouts of the logged users."
)
# subparser.add_argument("command", choices=["show", "allow", "deny"])

subsubparsers = subparser.add_subparsers(dest="command", required=True)

subsubparser = subsubparsers.add_parser(
    "allow", parents=[function, user_id], help="Reset timeout for a user."
)

subsubparser = subsubparsers.add_parser(
    "deny", parents=[function, user_id], help="Ban an existing user."
)

subsubparser = subsubparsers.add_parser(
    "show", parents=[function], help="Show the list of authorized users."
)

subsubparser = subsubparsers.add_parser(
    "list", parents=[], help="Show the list of registered functions."
)
