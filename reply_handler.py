import asyncio

from telethon import TelegramClient, events, functions
from telethon.types import User

import config


def say_hi(name):
    if name is None:
        message = 'Привет, рад, что вы откликнулись на вакансию 🔥\n'
    else:
        message = f'Привет {name}, рад, что вы откликнулись на вакансию 🔥\n'
    message = (
        message
        + 'Расскажите подробнее о вашем опыте работы, чтобы я смог узнать о вас побольше)'
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
client1 = TelegramClient('session_reply1', config.api_id, config.api_hash)
client2 = TelegramClient('session_reply2', config.api_id2, config.api_hash2)
client3 = TelegramClient('session_reply3', config.api_id2, config.api_hash2)

clients = [client1, client2, client3

           ]
my_client = TelegramClient('anon', config.my_api_id, config.my_api_hash)


@client1.on(events.NewMessage)
async def handle_new_message(event):
    try:
        if 'работа' == event.raw_text.lower():
            # print(event)
            bebra = await event.get_sender()
            await client1.loop.create_task(sent_reply(client1, bebra))
    except Exception as e:
        print(repr(e))
        # bebra = await my_client.get_entity(event.original_update.user_id)
        # print(bebra.first_name)

# replied = await event.get_reply_message()
# sender = replied.sender
# print(sender.username)
# # await event.answer(f'Hi, {sender.username}')
# await event.reply(f'hi, {sender}!')


async def check_new_messages():

    await client1.start()
    # request = await clients[0](functions.messages.GetDialogFiltersRequest())
    dialogs = client1.iter_dialogs()

    # ch = await client.get_entity(1515430527)
    # title = client(functions.channels.GetFullChannelRequest(channel=ch))
    # print(ch.title)

    # channels = await client.get_dialogs(folder=2)
    # for channel in channels:
    #     print(channel)
    #     print('\n\n')

    async for dialog in dialogs:
        # print(dialog.entity)
        try:
            if not isinstance(dialog.entity, User):
                continue
            if 'работа' == str(dialog.message.message).lower():
                bebra = dialog.entity
                await client1.loop.create_task(
                    sent_reply(client1, bebra)
                )

                # print(dialog.name)
        except Exception as e:
            print(repr(e))


async def sent_reply(client, bebra):

    print(bebra.first_name.split(' ')[0])
    await client.send_read_acknowledge(bebra.id)
    async with client.action(bebra, 'typing'):
        await asyncio.sleep(3)

        match bebra.first_name:
            case None:
                print('Новое сообщение is None')
                await client.send_message(bebra, say_hi(bebra.first_name))
            case _:
                await client.send_message(bebra, say_hi(bebra.first_name))
                print(f'Новое сообщение от: {bebra.first_name}')
        async with client.action(bebra, 'typing'):
            await asyncio.sleep(3)
            await client.send_message(bebra, reply_massage)
        print('reply message sent')


if __name__ == '__main__':
    # for client in clients[0]:
    # client1.start()
    try:
        client1.loop.run_until_complete(check_new_messages())
    except Exception as e:
        print(repr(e))
    client1.run_until_disconnected()
    # client.start()

    # with clients[0] as client:
    #     client.loop.run_until_complete(main())
    # with clients[0] as client:
    #     client.loop.run_until_complete(main())
