import asyncio

from telethon import TelegramClient, events
from telethon.types import User

import config


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


reply_massage = (
    'Кстати, вы можете пока заполнить форму,'
    ' которая пойдёт непосредственно директору для ознакомления.'
    'Вот ссылка на неё:\n'
    'https://docs.google.com/forms/d/e/'
    '1FAIpQLScQ4MXsn-Qrl38tRwgB6O5LPXrGt2Wasv8H5hCvA-N5H4w2Hw/viewform\n'
    'После этого отпишитесь, например "+", и мы продолжим диалог.'
)

reply_to_form = (
    'Отлично. Теперь ваша заявка рассмотрена и отправлена на утверждение '
    'директору. Если вы нам подойдёте, то я свяжусь с вами. '
    'И если у вас остались вопросы, то смело задавайте их!'
)


client1 = TelegramClient('session1', config.api_id, config.api_hash)
client2 = TelegramClient('session2', config.api_id2, config.api_hash2)
client3 = TelegramClient('session3', config.api_id2, config.api_hash2)
my_client = TelegramClient('anon', config.my_api_id, config.my_api_hash)

clients = [client1, client2, client3]

####################################################


def add_count(client):
    if client == client1:
        pass
    if client == client2:
        pass
    if client == client3:
        pass
####################################################


async def sent_reply_start(client, bebra):

    first_name = bebra.first_name.split(' ')[0]
    print(first_name)
    await client.send_read_acknowledge(bebra.id)
    async with client.action(bebra, 'typing'):
        await asyncio.sleep(4)
        await client.send_message(bebra, say_hi(bebra.first_name))
        print(f'Новое сообщение от: {bebra.first_name}')

    async with client.action(bebra, 'typing'):
        await asyncio.sleep(5)
        await client.send_message(bebra, reply_massage)
        print('reply message sent')


async def sent_reply_to_form(client, bebra):
    await client.send_read_acknowledge(bebra.id)
    async with client.action(bebra, 'typing'):
        await asyncio.sleep(5)
        await client.send_message(bebra, reply_to_form)
        print('form message sent')


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


@client1.on(events.NewMessage)
async def handle_new_message1(event):
    try:
        bebra = await event.get_input_sender()
        await match_sent_message(client1,
                                 bebra,
                                 event.raw_text.lower())
    except Exception as e:
        print(repr(e))


@client2.on(events.NewMessage)
async def handle_new_message2(event):
    try:
        bebra = await event.get_input_sender()
        print('lol ' + bebra.first_name)
        await match_sent_message(client2,
                                 bebra,
                                 event.raw_text.lower())
    except Exception as e:
        print(repr(e))


@client3.on(events.NewMessage)
async def handle_new_message3(event):
    try:
        # print(repr(client3.get_me()))
        bebra = await event.get_input_sender()
        await match_sent_message(client3,
                                 bebra,
                                 event.raw_text.lower())

    except Exception as e:
        print(repr(e))


####################################################


async def check_new_messages():

    try:
        await client.start()
        dialogs = client.iter_dialogs()
    except Exception as e:
        print(repr(e))

    async for dialog in dialogs:
        try:
            # if not isinstance(dialog.entity, User):
            #     continue
            bebra = dialog.entity
            await match_sent_message(client,
                                     bebra,
                                     str(dialog.message.message).lower())

            # print(dialog.name)
        except Exception as e:
            print(repr(e))


####################################################


def start_event_handler():
    try:
        loop = asyncio.get_event_loop()
        client1.start()
        client2.start()
        client3.start()
        loop.run_forever()
    except Exception as e:
        print(repr(e))


####################################################


if __name__ == '__main__':

    for current_client in clients:

        with current_client as client:
            client.session.save_entities = False
            client.loop.run_until_complete(check_new_messages())

    print('done')
    start_event_handler()
