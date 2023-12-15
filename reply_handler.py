import asyncio

import config

from loguru import logger
from messages_config import Reply
from telethon import events, TelegramClient
from telethon.types import User

# logger.remove()
logger.add(
    "process.log",
    format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="2 days",
    compression="zip",
)

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


async def match_sent_message(client, user, message):
    if not isinstance(user, User) or user.bot:
        return
    # logger.debug(user.username)
    if "заполнил" in message or "+" == message:
        await client.loop.create_task(sent_reply(client, user, Reply.FINISH))
        return
    elif any(key == message for key in ["работа", "ассистент"]):
        await client.loop.create_task(sent_reply_start(client, user))
        return


####################################################


@logger.catch
@client1.on(events.NewMessage)
async def handle_new_message1(event):
    bebra = await event.get_sender()
    await match_sent_message(client1, bebra, event.raw_text.lower())


@logger.catch
@client2.on(events.NewMessage)
async def handle_new_message2(event):
    bebra = await event.get_sender()
    await match_sent_message(client2, bebra, event.raw_text.lower())


@logger.catch
@client3.on(events.NewMessage)
async def handle_new_message3(event):
    bebra = await event.get_sender()
    await match_sent_message(client3, bebra, event.raw_text.lower())


####################################################


@logger.catch
async def check_new_messages():
    await client.start()
    dialogs = client.iter_dialogs()

    async for dialog in dialogs:
        try:
            bebra = dialog.entity
            message = str(dialog.message.message).lower()
            await match_sent_message(client, bebra, message)
        except ValueError as e:
            logger.critical(e.__class__.__name__)
            # print(dialog.name)
    logger.debug(show_client(client))


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
    try:
        logger.info("Begin check")
        for current_client in clients:
            with current_client as client:
                client.session.save_entities = False
                client.loop.run_until_complete(check_new_messages())
        logger.success("")
        start_event_handler()
    except Exception as e:
        logger.error(repr(e))
