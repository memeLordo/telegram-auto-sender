# from telethon.types import User
import asyncio

from config.messages import Lead
from loguru import logger
from telethon.types import User
from tools.editor import make_plain

from .clients import client1, client2, client3, show_client


async def start() -> None:
    bebra_set = []
    async for dialog in client1.iter_dialogs():
        if dialog.name == "Golubin | Assistant":
            golubin = dialog.entity
            break
    async for message in client1.iter_messages(entity=golubin):
        try:
            text_set = set(make_plain(message.message).split(" "))
            bebra = None
            for word in text_set:
                if word and "@" in word[0]:
                    nickname = word.strip("@")
                    if nickname is None:
                        continue

                    bebra = await client1.get_entity("@" + nickname)
                if not bebra or not isinstance(bebra, User) or bebra.bot:
                    continue
                if bebra in bebra_set:
                    continue
                logger.info(bebra.username)
                bebra_set.append(bebra)
            if len(bebra_set) == 50:
                global names_list
                names_list = bebra_set
                break
        except Exception:
            continue
        except TypeError:
            continue
    # await send_messages_to_leads(golubin, messages)


async def send_messages_to_leads(client, range_list, func):
    await client.start()
    for bebra in range_list:
        first_name = bebra.first_name.split(" ")[0]
        # await asyncio.sleep(1)
        # async with client.action(bebra, "typing"):
        await asyncio.sleep(4)
        await client.send_message(bebra, func(first_name))
        # print(func(first_name))
        logger.debug(
            f"{show_client(client)}: message sent to {bebra.username}")
    await client.disconnect()


def divide_names():
    k, _ = divmod(len(names_list), 2)
    first, second = names_list[:k], names_list[k:]
    return [first, second]


@logger.catch
def main() -> None:
    try:
        client1.start()
        client1.session.save_entities = False
        client1.loop.run_until_complete(start())
        client1.disconnect()
        names = divide_names()
        # global client

        asyncio.run(send_messages_to_leads(client2, names[0], Lead.say_hi))
        asyncio.run(send_messages_to_leads(client3, names[1], Lead.say_hi1))
    except KeyboardInterrupt:
        pass
