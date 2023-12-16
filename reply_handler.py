import asyncio
import string
import sys
from enum import auto, Enum

from loguru import logger
from messages_config import Keywords, Reply
from reply_walker import client1, client2, client3, run_message_checker
from telethon import events

# from telethon.types import User

# logger.remove()

logger.add(sys.stderr, level="TRACE")


####################################################


def add_count(client):
    if client == client1:
        pass
    if client == client2:
        pass
    if client == client3:
        pass


####################################################
class UserStatus(Enum):
    WAIT_FIRST_MESSAGE = "WAIT_FIRST_MESSAGE"
    WAIT_FORM = "WAIT_FORM"
    TROUBLE_FORM = "TROUBLE_FORM"
    DONE = "DONE"


class UserType(Enum):
    LEAD = "Lead"
    ASSISTANT = "Assistant"
    OTHER = "Other"


####################################################
state_database = {}
type_database = {}


def remove_punct(s):
    return s.translate(str.maketrans("", "", string.punctuation))


def define_type_by_message(event):
    form_message = remove_punct(event.text).lower()
    logger.trace(form_message)
    if any(key in form_message for key in Keywords.STARTING_MESSAGE):
        return UserType.ASSISTANT


def check_key_word(event, state):
    form_message = remove_punct(event.text).lower()
    match state:
        case UserStatus.WAIT_FORM:
            keywords = Keywords.FORM
            if not any(key in form_message for key in keywords):
                state_database[event.sender_id] = UserStatus.TROUBLE_FORM
        case UserStatus.TROUBLE_FORM:
            keywords = Keywords.TROUBLE + Keywords.FORM
            # await event.respond("Всё кончено.")
            # state_database[who] = UserStatus.FINISH
            pass
    if any(key in form_message for key in keywords):
        return True
    return False


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


async def run_handler(event):
    who = event.sender_id
    type_ = type_database.get(who)
    state_ = state_database.get(who)
    logger.trace(f"Type is {type_}")

    match type_:
        case None:
            type_database[who] = define_type_by_message(event)
            if type_database[who] == UserType.ASSISTANT:
                state_database[who] = UserStatus.WAIT_FIRST_MESSAGE
                await run_handler(event)
                return
        # TODO: проверять дальше, если не None
        case UserType.ASSISTANT:
            match state_:
                case UserStatus.WAIT_FIRST_MESSAGE:
                    await event.mark_read()
                    # await event.respond("Start message.")
                    state_database[who] = UserStatus.WAIT_FORM

                case UserStatus.WAIT_FORM | UserStatus.TROUBLE_FORM:
                    if check_key_word(event, state_):
                        await event.mark_read()
                        await event.respond("Отлично. Ожидайте результата!")
                        state_database[who] = UserStatus.DONE
                case UserStatus.TROUBLE_REPLY:
                    await event.mark_read()
                    await event.respond("Пожалуйста, сообщите, когда....")
                    state_database[who] = UserStatus.WAIT_FORM

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


####################################################


@logger.catch
def start_event_handler():
    logger.info("Begin loop")
    loop = asyncio.get_event_loop()
    client1.start()
    client2.start()
    client3.start()
    loop.run_forever()


####################################################
if __name__ == "__main__":
    run_message_checker()
    start_event_handler()
