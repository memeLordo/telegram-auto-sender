from enum import Enum


class UserStatus(Enum):
    WAIT_FIRST_MESSAGE = "WAIT_FIRST_MESSAGE"
    WAIT_FORM = "WAIT_FORM"
    # TROUBLE_FORM = "TROUBLE_FORM"
    DONE = "DONE"


class UserType(Enum):
    LEAD = "Lead"
    ASSISTANT = "Assistant"
    OTHER = "Other"
