from enum import Enum


class UserStatus(Enum):
    WAIT_FIRST_MESSAGE = "WAIT_FIRST_MESSAGE"
    WAIT_FORM_REPLY = "WAIT_FORM_REPLY"
    # TROUBLE_FORM = "TROUBLE_FORM"
    DONE = "DONE"


class UserType(Enum):
    LEAD = "Lead"
    ASSISTANT = "Assistant"
    OTHER = "Other"
