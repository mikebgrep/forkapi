from enum import Enum

class UserUpdateDetailsEnum(Enum):
    BOTH = 0,
    USERNAME = 1,
    EMAIL = 2,


class PasswordResetChoice(Enum):
    NUMERIC = 0,
    SHORT_ENTRY = 1,
    NON_MATCHING = 2,
