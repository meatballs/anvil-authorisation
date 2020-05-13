import functools

import anvil.users
from anvil.tables import app_tables

__version__ = "0.1.0"


def authentication_required(func):
    """A decorator to ensure only a valid user can call a server function"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if anvil.users.get_user() is None:
            raise ValueError("Authentication required")
        else:
            return func(*args, **kwargs)

    return wrapper


def authorisation_required(permissions):
    """A decorator to ensure a user has sufficient permissions to call a server function"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = anvil.users.get_user()
            if user is None:
                raise ValueError("Authentication required")
            if isinstance(permissions, str):
                required_permissions = set([permissions])
            else:
                required_permissions = set(permissions)
            try:
                user_permissions = set(
                    [
                        permission["name"]
                        for role in user["roles"]
                        for permission in role["permissions"]
                    ]
                )
            except TypeError:
                raise ValueError("Authorisation required")

            if not required_permissions.issubset(user_permissions):
                raise ValueError("Authorisation required")
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator
