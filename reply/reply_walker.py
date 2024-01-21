import asyncio
import datetime as dt
from datetime import date

from config.messages import Assistant, Deviation, Keywords
from loguru import logger
from telethon.types import Message, User
from tools.checker import is_user
from tools.editor import make_plain, remove_punct

from .clients import choose_clients, show_client
from .tags import UserStatus


class ExitLoop(Exception):
    pass


today: date = dt.date.today()

logger.add(
    "process.log",
    format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="2 days",
    compression="zip",
)


@logger.catch
async def sent_reply(bebra: User, message: str | Message) -> None:
    log_name: str = bebra.first_name
    await asyncio.sleep(1)
    await client.send_read_acknowledge(bebra)
    async with client.action(bebra, "typing"):
        await asyncio.sleep(4)
        await client.send_message(bebra, message)
        logger.debug(f"{show_client[client]}: message sent to {log_name}")


# Пока не знаю, какой объект возвращать
def filter_messages_by_date(messages: list) -> object | None:
    if messages.total > 5:
        return None
    return filter(
        lambda x: (today - x.date.date()).days <= Deviation.MESSAGE_AGE,
        messages,
    )


async def prepare_messages(by_user: User, from_user: User) -> object | None:
    return filter_messages_by_date(
        await client.get_messages(
            entity=by_user,
            from_user=from_user,
            limit=3,
        )
    )


def make_text_to_set(some_text: str) -> set:
    read_message: tuple[str] = tuple(make_plain(some_text).split(" "))
    return set(read_message)


def get_status_by(message: Message) -> UserStatus | None:
    message_ = make_text_to_set(message.message)
    form_ = make_text_to_set(Assistant.form())
    finish_ = make_text_to_set(make_plain(Assistant.FINISH))
    # TODO: change state
    if len(form_ & message_) / len(form_) >= Deviation.FORM:
        return UserStatus.WAIT_FORM_REPLY
    if len(finish_ & message_) / len(finish_) >= Deviation.FINISH:
        return UserStatus.DONE
    return None


# TODO: переписать в программу update_state.py
async def get_status_of(user: User):
    myself: User = await client.get_me()
    my_messages: list[Message] | None = await prepare_messages(user, myself)

    for message in my_messages or []:
        current_status: UserStatus | None = get_status_by(message)
        if current_status is None:
            continue
        return current_status
    return None


def update_status_by(message: str, prev_status: UserStatus):
    message_: set = make_text_to_set(message)
    logger.opt(colors=True).debug(f"<white>{message_}</white>")
    if not (message_ & Keywords.IGNORE):
        match prev_status:
            case None:
                if message_ & Keywords.FIRST_MESSAGE:
                    return UserStatus.WAIT_FIRST_MESSAGE
            case UserStatus.WAIT_FORM_REPLY:
                if message_ & Keywords.FORM:
                    return UserStatus.DONE
            case UserStatus.DONE:
                raise ExitLoop(prev_status)
    return prev_status


async def reply_by(user: User, message: str, status: UserStatus | None):
    new_status = update_status_by(message, status)
    if status != new_status:
        logger.opt(colors=True).debug(
            f"{user.username}: <red>{status} -> {new_status}</red>"
        )
    match new_status:
        case UserStatus.WAIT_FIRST_MESSAGE:
            first_name = remove_punct(user.first_name.split(" ")[0])
            await sent_reply(user, Assistant.form(first_name))
            logger.debug(f"Form message sent to {user.username}")
            # set_status -> W
        case UserStatus.DONE:
            await sent_reply(user, Assistant.FINISH)
            logger.debug(f"Finish message sent to {user.username}")
        case _:
            return
    raise ExitLoop(new_status)


async def match_messages(user: User) -> None:
    user_messages: list[Message] | None = await prepare_messages(user, user)

    if user_messages is None:
        return

    current_status: UserStatus | None = await get_status_of(user)
    for message in user_messages:
        message_text: str = message.message
        if not message_text:
            continue
        await reply_by(user, message_text, current_status)


@logger.catch
async def check_new_messages():
    await client.start()
    dialogs = await client.get_dialogs(ignore_pinned=True)
    filtered_dialogs = filter(
        lambda x: x.date is None
        or (today - x.date.date()).days <= Deviation.DIALOG_AGE,
        dialogs,
    )
    for dialog in filtered_dialogs:
        try:
            bebra: User = dialog.entity
            if not is_user(bebra):
                continue
            # logger.debug(bebra.username)
            # -> call func для внутр. проверки
            # -> call func для внеш. проверки
            # Проверяем статус по нашим полследним сообщениям из формы
            # Сначала назначим статус на основе наших сообщений в local_var,
            # а после будем делать запрос статуса уже внутри функции
            await match_messages(bebra)
        except ValueError as e:
            logger.critical(e.__class__.__name__)
        except ExitLoop as e:
            logger.success(f"{bebra.username} is {e}")

            # print(dialog.name)
    logger.debug(show_client[client])


@logger.catch
def run_message_checker() -> None:
    logger.info("Begin check")
    clients = choose_clients()
    for current_client in clients:
        global client
        with current_client as client:
            client.session.save_entities = False
            client.loop.run_until_complete(check_new_messages())
    logger.success("")


if __name__ == "__main__":
    try:
        run_message_checker()
        # start_event_handler()
    except KeyboardInterrupt:
        pass
