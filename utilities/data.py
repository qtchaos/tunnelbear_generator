import json
from dataclasses import dataclass


@dataclass
class Account:
    """Account class for storing account information."""
    email: str
    email_password: str
    password: str
    id: str


account = Account("test", "test", "test", "test")


class AccountEncoder(json.JSONEncoder):
    def default(self, object):
        return {"email": object.email, "email_password": object.email_password, "password": object.password}
