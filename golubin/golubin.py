import asyncio

# from telethon.types import User
from config.messages import Lead
from loguru import logger
from telethon import errors
from tools.checker import is_user
from tools.editor import make_plain

from .clients import client1, client2, client3, show_client
from .errors import form_error_list


async def make_user_list():
    golubin = await find_golubin()
    user_set = set()
    error_list = []
    async for message in client.iter_messages(entity=golubin):
        try:
            text_set = set(make_plain(message.message).split(" "))
            # logger.info(text_set)
            usernames = {wrd[1:] for wrd in text_set if wrd and wrd[0] == "@"}
            if usernames:
                logger.info(usernames)
                for username in usernames:
                    try:
                        first_name = await find_user_name(username)
                        if not first_name:
                            continue
                        user_set.add((username, first_name))
                    except errors.FloodWaitError as e:
                        global err_sec
                        err_sec = e.seconds
                        error_list.append((username, Lead.say_hi("ИМЯ")))
                        continue
                    except Exception as e:
                        logger.error(repr(e))
                        continue
            if len(error_list) >= 50:
                form_error_list(error_list, err_sec)
                return list()
            if len(user_set) >= 50:
                return list(user_set)
        except Exception as e:
            logger.error(repr(e))


async def find_user_name(username):
    user = await client.get_entity(username)
    if not is_user(user):
        return
    history = await client.get_messages(entity=user)
    history2 = await client3.get_messages(entity=user)
    await asyncio.sleep(3)
    if history or history2:
        return
    return user.first_name.split(" ")[0]


def divide_names(names_list):
    k, _ = divmod(len(names_list), 2)
    return names_list[:k], names_list[k:]


async def find_golubin():
    async for dialog in client.iter_dialogs():
        if dialog.name == "Golubin | Assistant":
            return dialog.entity


# async def start():
#     result = await make_user_list()
#     return result
# user = await client.get_entity("ram_tim")
# await client.send_message(user, Lead.say_hi("Рамилия"))


async def send_messages_in_list(range_list):
    for username, name in range_list:
        bebra = await client.get_entity(username)
        await asyncio.sleep(60)
        await client.send_message(bebra, Lead.say_hi(name))
        logger.debug(f"{show_client(client)}:message sent to {username}")
    await client.disconnect()


@logger.catch
def main() -> None:
    try:
        client2.start()
        client3.start()
        global client
        with client1 as client:
            client.session.save_entities = False
            user_list = client.loop.run_until_complete(make_user_list())
        first, second = divide_names(user_list)
        with client2 as client:
            client.loop.run_until_complete(send_messages_in_list(first))
        with client3 as client:
            client.loop.run_until_complete(send_messages_in_list(second))
        logger.info("done")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
