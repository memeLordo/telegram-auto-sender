import asyncio

from telethon import TelegramClient, events

import config

# from translate import Translator


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


@my_client.on(events.NewMessage)
async def handle_new_message(event):
    if 'работа' in event.raw_text.lower():
        # print(event)
        bebra = await event.get_sender()
        print(f'Новое сообщение от: {bebra.first_name}')
        # bebra = await my_client.get_entity(event.original_update.user_id)
        # print(bebra.first_name)
        await my_client.send_read_acknowledge(bebra.id, event.message)
        async with my_client.action(bebra, 'typing'):
            await asyncio.sleep(10)
            await my_client.send_message(bebra, f'Привет, {bebra.first_name}')

        # replied = await event.get_reply_message()
        # sender = replied.sender
        # print(sender.username)
        # # await event.answer(f'Hi, {sender.username}')
        # await event.reply(f'hi, {sender}!')


if __name__ == '__main__':
    my_client.start()
    my_client.run_until_disconnected()
