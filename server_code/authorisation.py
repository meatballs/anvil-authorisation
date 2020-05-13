import anvil.users
from anvil.tables import app_tables
import functools
import anvil.users


# def auth_required(func):
#     @functools.wraps(func)
#     def wrapped(*args, **kwargs):
#         if not anvil.users.get_user():
#             raise ValueError("Authentication required")
#         else:
#             return func(*args, **kwargs)

#     return wrapped
  
  
class authentication_required:
    """A decorator to ensure only a valid user can call a server function"""
    def __call__(self, func):
        if anvil.users.get_user() is None:
            raise ValueError("Authentication required")
        else:
            return func(*args, **kwargs)

          
class authorisation_required:
    """A decorator to ensure a user has sufficient permissions to call a server function"""
    def __init__(self, permissions):
        if isinstance(permissions, str):
            permissions = [permissions]
        self.required_permissions = permissions
        
    def __call__(self, func):
        user = anvil.users.get_user()
        if user is None:
            raise ValueError("Authentication required")
        user_permissions = set([
            permission["name"]
            for role in user["roles"]
            for permission in role["permissions"]
        ])
        

def permission_required(permissions):
    def permission_required_decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            user = anvil.users.get_user()
            if isinstance(permissions, str):
                all_permissions = [permissions]
            else:
                all_permissions = permissions
            permissions_row = (app_tables.permissions.get(user=user)) or (
                app_tables.permissions.add_row(user=user)
            )
            has_permission = all(
                [permissions_row[permission] for permission in all_permissions]
            )
            if not has_permission:
                raise ValueError("Permission required")
            else:
                return func(*args, **kwargs)

        return wrapped

    return permission_required_decorator
