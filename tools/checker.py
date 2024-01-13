from telethon.types import User


def is_user(user: User) -> bool:
    return isinstance(user, User) and not user.bot
