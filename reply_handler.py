import asyncio

from telethon import TelegramClient, events, functions, utils
from telethon.types import User

import config


def say_hi(name):
    if name is None:
        return 'Привет, рад, что вы откликнулись на вакансию 🔥'

    return f'Привет {name}, рад, что вы откликнулись на вакансию 🔥'


reply_massage = (
    'Кстати, вы можете пока заполнить форму,'
    ' которая пойдёт непосредственно директору для ознакомления.'
    'Вот ссылка на неё:\n'
    'https://docs.google.com/forms/d/e/'
    '1FAIpQLScQ4MXsn-Qrl38tRwgB6O5LPXrGt2Wasv8H5hCvA-N5H4w2Hw/viewform\n'
    'После этого отпишитесь, например "+", и мы продолжим диалог.'
)
#
# translator = Translator(from_lang='English', to_lang='russian')
#
# text_Eng = input('что перевести ')
#
# text_Rus = translator.translate(text_Eng)
#
# print(text_Rus)


clients = [
    TelegramClient('session1', config.api_id, config.api_hash),
    TelegramClient('session2', config.api_id2, config.api_hash2),
    TelegramClient('session3', config.api_id2, config.api_hash2),
]
my_client = TelegramClient('anon', config.my_api_id, config.my_api_hash)


@clients[0].on(events.NewMessage)
@clients[1].on(events.NewMessage)
@clients[2].on(events.NewMessage)
async def handle_new_message(event):
    if 'работа' in event.raw_text.lower():
        # print(event)
        bebra = await event.get_sender()
        # bebra = await my_client.get_entity(event.original_update.user_id)
        # print(bebra.first_name)
        await client.send_read_acknowledge(bebra.id, event.message)
        async with my_client.action(bebra, 'typing'):
            await asyncio.sleep(10)

            match bebra.first_name:
                case None:
                    print('Новое сообщение is None')
                case _:
                    await my_client.send_message(
                        bebra, say_hi(bebra.first_name)
                    )
                    print(f'Новое сообщение от: {bebra.first_name}')
        async with my_client.action(bebra, 'typing'):
            await asyncio.sleep(10)
            await my_client.send_message(bebra, reply_massage)
            print('reply message sent')

            # replied = await event.get_reply_message()
        # sender = replied.sender
        # print(sender.username)
        # # await event.answer(f'Hi, {sender.username}')
        # await event.reply(f'hi, {sender}!')


async def check_new_messages():

    # request = await clients[0](functions.messages.GetDialogFiltersRequest())
    # dialogs = client.iter_dialogs()

    ch = await client.get_entity(1515430527)
    # title = client(functions.channels.GetFullChannelRequest(channel=ch))
    print(ch.title)

    # channels = await client.get_dialogs(folder=2)
    # for channel in channels:
    #     print(channel)
    #     print('\n\n')

    async for dialog in client.iter_dialogs():
        # print(dialog.entity)
        try:
            if not isinstance(dialog.entity, User):
                continue
            if 'работа' in str(dialog.message.message).lower():
                bebra = dialog.entity
                print(bebra.first_name.split(' ')[0])
                # await client.send_read_acknowledge(bebra.id)
                # async with my_client.action(bebra, 'typing'):
                #     await asyncio.sleep(10)
                #
                #     match bebra.first_name:
                #         case None:
                #             print('Новое сообщение is None')
                #         case _:
                #             await my_client.send_message(
                #                 bebra, say_hi(bebra.first_name)
                #             )
                #             print(f'Новое сообщение от: {bebra.first_name}')
                # async with my_client.action(bebra, 'typing'):
                #     await asyncio.sleep(10)
                #     await my_client.send_message(bebra, reply_massage)
                print('reply message sent')
                # print(dialog.name)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # for client in clients[0]:
    with clients[0] as client:
        client.start()
        client.loop.run_until_complete(check_new_messages())
        client.run_until_disconnected()

# with clients[0] as client:
#     client.loop.run_until_complete(main())
