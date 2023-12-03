import asyncio

from loguru import logger
from telethon import TelegramClient, events
from telethon.types import User

import config
from messages_config import reply_massage, reply_to_form

# logger.remove()
logger.add(
    "process.log",
    format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="2 days",
    compression="zip"
)

####################################################


def say_hi(name):
    if name is None:
        message = 'Привет, рад, что вы откликнулись на вакансию 🔥\n'
    else:
        message = f'Привет {name}, рад, что вы откликнулись на вакансию 🔥\n'
    message = (
        message
        + 'Расскажите подробнее о вашем опыте работы,' +
        ' чтобы я смог узнать о вас побольше)'
    )
    return message


####################################################

client1 = TelegramClient('session1', config.api_id, config.api_hash)
client2 = TelegramClient('session2', config.api_id2, config.api_hash2)
client3 = TelegramClient('session3', config.api_id2, config.api_hash2)
my_client = TelegramClient('anon', config.my_api_id, config.my_api_hash)

clients = [client1, client2, client3]

####################################################


def show_client(client):
    if client == client1:
        return 'client1'
    elif client == client2:
        return 'client2'
    else:
        return 'client3'


def add_count(client):
    if client == client1:
        pass
    if client == client2:
        pass
    if client == client3:
        pass


####################################################


async def sent_reply_start(client, bebra):

    logger.info(f'{show_client(client)}: got message from {bebra.first_name}')

    first_name = bebra.first_name.split(' ')[0]
    await client.send_read_acknowledge(bebra.id)
    async with client.action(bebra, 'typing'):
        await asyncio.sleep(4)
        await client.send_message(bebra, say_hi(first_name))

    async with client.action(bebra, 'typing'):
        await asyncio.sleep(5)
        await client.send_message(bebra, reply_massage)
        logger.info(
            f'{show_client(client)}: message sent to {bebra.first_name}')


async def sent_reply_to_form(client, bebra):

    logger.info(f'{show_client(client)}: got message from {bebra.first_name}')

    await client.send_read_acknowledge(bebra.id)
    async with client.action(bebra, 'typing'):
        await asyncio.sleep(5)
        await client.send_message(bebra, reply_to_form)
        logger.info(
            f'{show_client(client)}: message sent to {bebra.first_name}')


####################################################


async def match_sent_message(client, user, message):
    if not isinstance(user, User):
        return
    match message:
        case 'работа' | 'ассистент':
            await client.loop.create_task(
                sent_reply_start(client, user)
            )
        case '+':
            await client.loop.create_task(
                sent_reply_to_form(client, user)
            )


####################################################

@logger.catch
@client1.on(events.NewMessage)
async def handle_new_message1(event):
    try:
        bebra = await event.get_sender()
        await asyncio.sleep(1)
        await match_sent_message(client1,
                                 bebra,
                                 event.raw_text.lower())
    except ValueError:
        logger.error(bebra.first_name + ' is muted')
        logger.info('Running through the messages')
        client1.loop.run_until_complete(check_new_messages())
    # except Exception as e:
    #     logger.critical(repr(e))


@logger.catch
@client2.on(events.NewMessage)
async def handle_new_message2(event):
    try:
        bebra = await event.get_sender()
        await asyncio.sleep(1)
        await match_sent_message(client2,
                                 bebra,
                                 event.raw_text.lower())
    except ValueError:
        logger.error(bebra.first_name + ' is muted')
        logger.info('Running through the messages')
        client2.loop.run_until_complete(check_new_messages())
    # except Exception as e:
    #     logger.critical(repr(e))


@logger.catch
@client3.on(events.NewMessage)
async def handle_new_message3(event):
    try:
        # print(client3)
        bebra = await event.get_sender()
        await asyncio.sleep(1)
        await match_sent_message(client3,
                                 bebra,
                                 event.raw_text.lower())
    except ValueError:
        logger.error(bebra.first_name + ' is muted')
        logger.info('Running through the messages')
        client3.loop.run_until_complete(check_new_messages())
    # except Exception as e:
    #     logger.critical(repr(e))


####################################################


@logger.catch
async def check_new_messages():

    await client.start()
    dialogs = client.iter_dialogs()
    # except Exception as e:
    #     print(repr(e))
    #
    async for dialog in dialogs:
        try:
            bebra = dialog.entity
            await match_sent_message(client,
                                     bebra,
                                     str(dialog.message.message).lower())
        except ValueError as e:
            logger.critical(e.__class__.__name__)
            # print(dialog.name)
        # except Exception as e:
        #     print(repr(e))
    logger.info(show_client(client))


####################################################


@logger.catch
def start_event_handler():
    # try:
    logger.info('Begin loop')
    loop = asyncio.get_event_loop()
    client1.start()
    client2.start()
    client3.start()
    loop.run_forever()
    # except Exception as e:
    #     print(repr(e))


####################################################


if __name__ == '__main__':

    for current_client in clients:

        with current_client as client:
            client.session.save_entities = False
            client.loop.run_until_complete(check_new_messages())

    logger.success('')
    start_event_handler()
