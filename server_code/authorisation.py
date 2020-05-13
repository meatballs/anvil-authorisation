import anvil.users
from anvil.tables import app_tables
import functools
import anvil.users

  
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
        self.required_permissions = set(permissions)
        
    def __call__(self, func, *args, **kwargs):
        user = anvil.users.get_user()
        if user is None:
            raise ValueError("Authentication required")
        user_permissions = set([
            permission["name"]
            for role in user["roles"]
            for permission in role["permissions"]
        ])
        if not self.required_permissions.issubset(user_permissions):
            raise ValueError("Authorisation required")
        else:
            return func(*args, **kwargs)