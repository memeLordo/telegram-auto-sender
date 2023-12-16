import asyncio
import string
import sys
from enum import auto, Enum

import config
from loguru import logger
from messages_config import Reply
from telethon import events, TelegramClient

# from telethon.types import User

# logger.remove()
logger.add(
    "process.log",
    format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="2 days",
    compression="zip",
)
logger.add(sys.stderr, level="TRACE")
####################################################

####################################################

client1 = TelegramClient("r_session1", config.api_id, config.api_hash)
client2 = TelegramClient("r_session2", config.api_id2, config.api_hash2)
client3 = TelegramClient("r_session3", config.api_id2, config.api_hash2)
my_client = TelegramClient("anon", config.my_api_id, config.my_api_hash)

clients = [client1, client2, client3]

####################################################


def show_client(client):
    if client == client1:
        return "client1"
    elif client == client2:
        return "client2"
    else:
        return "client3"


def add_count(client):
    if client == client1:
        pass
    if client == client2:
        pass
    if client == client3:
        pass


####################################################


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

    # except errors.rpcerrorlist.RpcCallFailError:
    #     logger.error('Telegram is Down. Reloading...')
    #     client.disconnect()
    #     await client.start()
    #     async with client:
    #         await client.loop.run_until_complete(check_new_messages())
    #############


@logger.catch
async def sent_reply(client, bebra, message, error_exit=False):
    log_name = bebra.first_name
    sender = bebra.username
    logger.info(f"{show_client(client)}: got message from {log_name}")
    await asyncio.sleep(1)

    #############
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
    #############


####################################################
keywords = ["гладиолус"]


def remove_punct(s):
    return s.translate(str.maketrans("", "", string.punctuation))


def define_type_by_message(message):
    form_message = remove_punct(message).lower()
    logger.trace(form_message)
    if any(key in form_message for key in keywords):
        return UserType.ASSISTANT


def check_key_word(event, state):
    match state:
        case None:
            pass


# async def match_sent_message(client, user, message):
#     if not isinstance(user, User) or user.bot:
#         return
#     # logger.debug(user.username)
#     if "заполнил" in message or "+" == message:
#         await client.loop.create_task(sent_reply(client, user, Reply.FINISH))
#         return
#     elif any(key == message for key in ["работа", "ассистент"]):
#         await client.loop.create_task(sent_reply_start(client, user))
#         return


####################################################
class UserStatus(Enum):
    INIT_ = auto()
    WAIT_FORM = auto()
    FINISH = auto()
    DONE = auto()


class UserType(Enum):
    LEAD = auto()
    ASSISTANT = auto()
    OTHER = auto()


state_database = {}
type_database = {}


async def run_handler(event):
    who = event.sender_id
    type_ = type_database.get(who)
    state_ = state_database.get(who)
    logger.trace(f"Type is {type_}")

    match type_:
        case None:
            type_database[who] = define_type_by_message(event.text)
            if type_database[who] == UserType.ASSISTANT:
                await run_handler(event)
                return
        # TODO: проверять дальше, если не None
        case UserType.ASSISTANT:
            match state_:
                case None:
                    state_database[who] = UserStatus.WAIT_FORM
                    await event.mark_read()
                    # await event.respond("Start message.")
                case UserStatus.WAIT_FORM:
                    if check_key_word(event, state_):
                        await event.mark_read()
                        await event.respond("Подожди.")
                    state_database[who] = UserStatus.FINISH

                case UserStatus.FINISH:
                    if check_key_word(event, state_):
                        await event.mark_read()
                        await event.respond("Чем могу помочь?")
                        state_database[who] = UserStatus.DONE

                case UserStatus.DONE:
                    # await event.respond("Всё кончено.")
                    # state_database[who] = UserStatus.FINISH
                    pass
                case _:
                    # TODO: отправить сообщение мне с этого аккаунта.
                    pass
            logger.info(state_database[who])

        case UserType.LEAD:
            pass


@logger.catch
# @client1.on(events.NewMessage(func=lambda e: e.is_private))
# @client2.on(events.NewMessage(func=lambda e: e.is_private))
@client3.on(events.NewMessage(func=lambda e: e.is_private))
async def handler(event):
    # sender = await event.get_sender()
    # print(event)

    await run_handler(event)
    #
    #     case UserState.WAIT_FORM:
    #         name = event.text  # Save the name wherever you want
    #         await event.respond(Reply.FORM)
    #         state_database[who] = UserState.WAIT_AGE
    #
    #     case UserState.WAIT_AGE:
    #         age = event.text  # Save the age wherever you want
    #         await event.respond(Reply.FINISH)
    #         # Conversation is done so we can forget the state of this user
    #         del state_database[who]


####################################################


@logger.catch
async def check_new_messages():
    await client.start()
    dialogs = client.iter_dialogs()
    print(dialogs)

    # async for dialog in dialogs:
    #     try:
    #         bebra = dialog.entity
    #         message = str(dialog.message.message).lower()
    #         await match_sent_message(client, bebra, message)
    #     except ValueError as e:
    #         logger.critical(e.__class__.__name__)
    #         # print(dialog.name)
    # logger.debug(show_client(client))


####################################################


@logger.catch
def start_event_handler():
    logger.info("Begin loop")
    loop = asyncio.get_event_loop()
    client1.start()
    client2.start()
    client3.start()
    loop.run_forever()


@logger.catch
def run_message_checker():
    logger.info("Begin check")
    for current_client in clients:
        global client
        with current_client as client:
            client.session.save_entities = False
            client.loop.run_until_complete(check_new_messages())
    logger.success("")


####################################################


if __name__ == "__main__":
    run_message_checker()
    start_event_handler()
