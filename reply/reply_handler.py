import asyncio
import sys

from config.messages import Assistant, Keywords

from loguru import logger
from telethon import events
from telethon.types import Event, User
from tools.editor import remove_punct

from .clients import client1, client2, client3
from .tags import UserStatus, UserType


logger.remove()
logger.add(sys.stderr, level="TRACE")


state_database = {}
type_database = {}


def define_type_by_message(event: Event) -> UserType:
    message_set = set(remove_punct(event.text).lower().split(" "))
    logger.trace(message_set)
    if message_set & Keywords.FIRST_MESSAGE:
        return UserType.ASSISTANT


def check_key_word(event: Event, state: UserStatus) -> bool:
    message_set = set(remove_punct(event.text).lower().split(" "))

    if message_set & Keywords.FORM:
        return True
    return False


####################################################


async def run_handler(event: Event) -> None:
    who: int = event.sender_id
    sender: User = await event.get_sender()
    type_: dict = type_database.get(who)
    state_: dict = state_database.get(who)
    logger.trace(f"Type is {type_}")

    match type_:
        case None:
            # TODO: set type function
            type_database[who] = define_type_by_message(event)
            if type_database[who] == UserType.ASSISTANT:
                state_database[who] = UserStatus.WAIT_FIRST_MESSAGE
                await run_handler(event)
                return
        # TODO: проверять дальше, если не None
        case UserType.ASSISTANT:
            match state_:
                case UserStatus.WAIT_FIRST_MESSAGE:
                    sender_name = sender.first_name.split(" ")[0]
                    await asyncio.sleep(1)
                    await event.mark_read()
                    async with event.client.action(sender, "typing"):
                        await asyncio.sleep(4)
                        await event.respond(Assistant.form(sender_name))
                    # TODO: change status to function
                    state_database[who] = UserStatus.WAIT_FORM_REPLY

                case UserStatus.WAIT_FORM_REPLY:
                    if check_key_word(event, state_):
                        await asyncio.sleep(1)
                        await event.mark_read()
                        async with event.client.action(sender, "typing"):
                            await asyncio.sleep(4)
                            await event.respond(Assistant.FINISH)
                        # TODO: change status to function
                        state_database[who] = UserStatus.DONE
                # case UserStatus.TROUBLE_REPLY:
                #     await event.mark_read()
                #     await event.respond("Пожалуйста, сообщите, когда....")
                #     state_database[who] = UserStatus.WAIT_FORM_REPLY

                case UserStatus.DONE:
                    # await event.respond("Всё кончено.")
                    # state_database[who] = UserStatus.FINISH
                    pass
                case _:
                    # TODO: отправить сообщение мне с этого аккаунта.
                    pass
            # TODO: return status function
            logger.info(state_database[who])

        case UserType.LEAD:
            pass


@logger.catch
# @client1.on(events.NewMessage(func=lambda e: e.is_private))
# @client2.on(events.NewMessage(func=lambda e: e.is_private))
@client3.on(events.NewMessage(func=lambda e: e.is_private))
async def handler(event: Event) -> None:
    # sender = await event.get_sender()
    # print(event)
    await run_handler(event)


####################################################


@logger.catch
def start_event_handler() -> None:
    logger.info("Begin loop")
    loop = asyncio.get_event_loop()
    client1.start()
    client2.start()
    client3.start()
    loop.run_forever()


####################################################
if __name__ == "__main__":
    try:
        # run_message_checker()
        start_event_handler()
    except KeyboardInterrupt:
        pass
