import asyncio
import datetime as dt

from config.messages import Keywords, Reply
from loguru import logger
from telethon.types import User
from tools.editor import make_plain

from .clients import choose_clients, show_client
from .tags import UserStatus


class ExitLoop(Exception):
    pass


today = dt.date.today()
max_msg_age = 14

logger.add(
    "process.log",
    format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="2 days",
    compression="zip",
)


@logger.catch
async def sent_reply_start(client, bebra, error_exit=False):
    log_name = bebra.first_name
    first_name = bebra.first_name.split(" ")[0]
    sender = bebra.username
    if not error_exit:
        logger.info(f"{show_client(client)}: got message from {log_name}")

    await asyncio.sleep(1)

    #############
    try:
        await client.send_read_acknowledge(sender)
        async with client.action(bebra, "typing"):
            await asyncio.sleep(4)
            await client.send_message(bebra, Reply.say_hi(first_name))

        async with client.action(bebra, "typing"):
            await asyncio.sleep(5)
            await client.send_message(sender, Reply.FORM)
            logger.debug(f"{show_client(client)}: message sent to {log_name}")

    except ValueError:
        logger.error(f"{show_client(client)}: {log_name} is unknown")

        if error_exit:
            raise ValueError(f"{show_client(client)}: Still unresolved")

        dialogs = client.iter_dialogs()
        async for dialog in dialogs:
            try:
                if dialog.entity.id == bebra.id:
                    logger.info(f"{log_name}'s ID found")
                    bebra = dialog.entity
                    # logger.debug(bebra)
                    await sent_reply_start(client, bebra, True)
                    break
            except Exception as e:
                logger.critical(repr(e))


@logger.catch
async def sent_reply(client, bebra, message, error_exit=False):
    log_name = bebra.first_name
    sender = bebra.username
    logger.info(f"{show_client(client)}: got message from {log_name}")
    await asyncio.sleep(1)

    try:
        await client.send_read_acknowledge(sender)

        async with client.action(bebra.username, "typing"):
            await asyncio.sleep(4)
            await client.send_message(sender, message)
            logger.debug(f"{show_client(client)}: message sent to {log_name}")
    except ValueError:
        logger.error(f"{show_client(client)}: {log_name} is unknown")

        if error_exit:
            raise ValueError(f"{show_client(client)}: Still unresolved")

        dialogs = client.iter_dialogs()
        async for dialog in dialogs:
            try:
                if dialog.entity.id == bebra.id:
                    logger.info(f"{log_name}'s ID found")
                    bebra = dialog.entity
                    # logger.debug(bebra)
                    await sent_reply(client, bebra, message, True)
                    break
            except Exception as e:
                logger.critical(repr(e))


async def match_sent_message(client, user, from_user, message, c_state=None):
    read_message = make_plain(message.message).split(" ")
    r_message = set(read_message)
    if user != from_user:
        form_set = set(make_plain(Reply.FORM).split(" "))
        finish_set = set(make_plain(Reply.FINISH).split(" "))
        # TODO: change state
        if len(form_set & r_message) / len(form_set) >= 0.7:
            raise ExitLoop(f"{user.username} = {UserStatus.WAIT_FORM}")
        if len(finish_set & r_message) / len(finish_set) == 1:
            raise ExitLoop(f"{user.username} = {UserStatus.DONE}")
        return

    logger.opt(colors=True).debug(
        f"<white>{read_message}</white> : {user.username}")
    upprove = Keywords.FIRST_MESSAGE
    ignore = Keywords.IGNORE
    if r_message & upprove and not (r_message & ignore):
        match c_state:
            case None:
                raise ExitLoop(f"First message sent to {user.username}")
                # TODO: send start_message to user
        # await sent_reply_start(client, user)


async def match_messages_from(client, user, from_user):
    user_messages = await client.get_messages(
        entity=user,
        from_user=from_user,
        limit=3,
        # reverse=True,
    )
    if user_messages.total > 5:
        return
    user_messages = filter(
        lambda x: (today - x.date.date()).days <= max_msg_age, user_messages
    )

    for message in user_messages:
        if not message.message:
            continue
        await match_sent_message(client, user, from_user, message)


@logger.catch
async def check_new_messages():
    await client.start()
    global myself
    myself = await client.get_me()
    dialogs = client.iter_dialogs()

    async for dialog in dialogs:
        try:
            bebra = dialog.entity
            if not isinstance(bebra, User) or bebra.bot:
                continue
            logger.debug(bebra.username)
            # Проверяем статус по нашим полследним сообщениям из формы
            await match_messages_from(client, bebra, myself)

            # Далее определяем тип по последним сообщениям пользователя
            await match_messages_from(client, bebra, bebra)

        except ValueError as e:
            logger.critical(e.__class__.__name__)
        except ExitLoop as e:
            logger.success(repr(e))
            # print(dialog.name)
    logger.debug(show_client(client))


@logger.catch
def run_message_checker():
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
