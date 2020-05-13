# Anvil Authentication and Role Based Authorisation
#
# Copyright (C) 2020 Owen Campbell
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# This program is published at https://github.com/meatballs/anvil-authorisation
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
