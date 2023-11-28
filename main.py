# import json
import asyncio

from telethon import errors, functions
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel

import config

# Use your own values from my.telegram.org

clients = [
    TelegramClient('session1', config.api_id, config.api_hash),
    TelegramClient('session2', config.api_id2, config.api_hash2),
    TelegramClient('session3', config.api_id2, config.api_hash2),
]

SEARCHED_DIRS = ['Новые FA', 'Free assist']
ad_1 = str(
    '#Вакансия #ищуассистента\n'
    '\n'
    '🔍 Ищу ассистента: удаленно\n'
    'Это отличная возможность получить ценный опыт в сфере поставок товаров,\n'
    'развития новых бизнес - направлений в компании с 7 - им стажем💥'
    '\n'
    'Задачи, которые тебя ждут:\n'
    '    - Ведение документооборота\n'
    '    - Поиск информации в интернете\n'
    '    - Работа в excel таблицах\n'
    '    - Личные поручения\n'
    '\n'
    'Условия:\n'
    '-  График работы: 4 часа в день\n'
    '-  Выходные сб и вс\n'
    '-  Полностью удаленная работа\n'
    '-  Недельная стажировка\n'
    '-  ЗП 20000 р\n'
    '-  Есть возможность карьерного роста до менеджера по проектам\n'
    '\n'
    'Если ты имеешь:\n'
    '✔️ Опыт работы с офисными приложениями(Word, Excel).\n'
    '✔️ Ответственно подходишь к работе\n'
    '✔️ Быстро обучаешься новому\n'
    '\n'
    '👉 То  пиши "РАБОТА" @behetly',
)
ad_2 = str(
    '🔍 Ищу ассистента: удаленно\n'
    'Это отличная возможность получить ценный опыт в сфере поставок товаров\n'
    'развития новых бизнес - направлений в компании с 7 - им стажем💥\n'
    '\n'
    ' Задачи, которые тебя ждут:\n'
    ' - Ведение документооборота\n'
    ' - Поиск информации в интернете\n'
    '-  Работа в excel таблицах\n'
    ' - Личные поручения\n'
    '\n'
    'Условия:\n'
    '-  График работы: 4 часа в день\n'
    '-  Выходные сб и вс\n'
    '-  Полностью удаленная работа\n'
    '-  Недельная стажировка\n'
    '-  ЗП 20000 р\n'
    '-  Есть возможность карьерного роста до менеджера по проектам\n'
    '\n'
    'Если ты имеешь:\n'
    '✔️ Опыт работы с офисными приложениями (Word, Excel).\n'
    '✔️ Ответственно подходишь к работе\n'
    '✔️ Быстро обучаешься новому\n'
    '\n'
    '👉 То  пиши "РАБОТА" ЛС'
)


async def main():
    request = await client(functions.messages.GetDialogFiltersRequest())
    await send_to_channels(request)

    # async for dialog in client.iter_dialogs():
    #     print(dialog.id)
    #     print(client.get_entity(GetFullChannel(dialog.id)))
    # if dialog.id in ad_channels_1:
    #     print('success')
    # if dialog.name == 'Golubin | Assistant':
    #     print(dialog.id)
    # await send_to_channels(SEARCHED_DIRS)


async def send_to_channels(request, dirs=SEARCHED_DIRS):
    for dialog_filter in request:
        result = dialog_filter.to_dict()
        try:
            title = result['title']

            if title in dirs:
                print(result['title'])

                match title:
                    case 'Free assist':
                        await send_message_to_channel(result, ad_1)
                        await asyncio.sleep(3)
                        print('Succsess')

                    case 'Новые FA':
                        await send_message_to_channel(result, ad_2)
                        await asyncio.sleep(3)
                        print('Отправлено 2.')

        except KeyError:
            pass


#
#     for dialog_filter in request:
#         result = dialog_filter.to_dict()
#         try:
#             title = result['title']
#
#             if title in dirs:
#                 print(result['title'])
#
#                 match title:
#                     case 'Free assist':
#                         await send_message_to_channel(result, ad_1)
#                         print('Отправлено 1.')
#
#                     case 'Новые FA':
#                         await send_message_to_channel(result, ad_2)
#                         print('Отправлено 2.')
#
#         except KeyError:
#             pass
# print(json.dumps(result))


async def send_message_to_channel(result, message):
    for channel in result['pinned_peers'] + result['include_peers']:
        try:

            channel_id = int(channel['channel_id'])
            # if channel_id in Skip_List:
            #     raise Exception(f'id {channel_id} skipeed')

            access_hash = int(channel['access_hash'])

            get_channel = InputPeerChannel(
                channel_id=channel_id, access_hash=access_hash
            )
            async with client.action(channel_id=channel_id, 'typing'):
                await client.send_message(get_channel, message=message)
            await asyncio.sleep(1)
            print(f'sent to {get_channel}')

        except KeyError:
            pass
        except errors.rpcbaseerrors.ForbiddenError as e:
            print(e)
        except errors.rpcerrorlist.UserBannedInChannelError as e:
            print(e)
        except errors.rpcerrorlist.ChannelPrivateError as e:
            print(e)
        except errors.rpcerrorlist.SlowModeWaitError:
            continue
        except Exception as e:
            print(e)

    # for channel in :
    #     try: w
    #         asyncio.sleep(1)
    #         channel_id = int(channel['channel_id'])
    #         # await client.send_message(channel_id, message=message)
    #         print(f'sent to {channel_id}')
    #     except KeyError:
    #         pass
    #     except errors.rpcbaseerrors.ForbiddenError as e:
    #         print(e)
    #     except errors.rpcerrorlist.UserBannedInChannelError as e:
    #         print(e)


for current_client in clients:
    with current_client as client:
        client.session.save_entities = False
        client.loop.run_until_complete(main())
        await asyncio.sleep(10 * 60)
