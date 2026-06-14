from dataclasses import dataclass


@dataclass
class User:
    name: str
    user_id: str
    email: str
    phone: str
