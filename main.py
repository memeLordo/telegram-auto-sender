# import json
import asyncio

from telethon import errors, functions
from telethon.sync import TelegramClient
from telethon.tl import types

import config
from messages_config import ad_1, ad_2

clients = [
    TelegramClient('session1', config.api_id, config.api_hash),
    TelegramClient('session2', config.api_id2, config.api_hash2),
    TelegramClient('session3', config.api_id2, config.api_hash2),
]

SEARCHED_DIRS = ['Новые FA', 'Free assist']
count = 0


async def main():
    request = await client(functions.messages.GetDialogFiltersRequest())

    await send_to_channels(request)

    print(count)
    if client != clients[-1]:
        print('start waiting')
        await asyncio.sleep(10 * 60)

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
                # await send_message_to_channel(result, ad_kazan)
                await asyncio.sleep(3)

                match title:
                    case 'Free assist':
                        await send_message_to_channel(result, ad_1)
                        await asyncio.sleep(3)

                    case 'Новые FA':
                        await send_message_to_channel(result, ad_2)
                        await asyncio.sleep(3)

                print('Succsess')

        except KeyError:
            pass


async def send_message_to_channel(result, message):
    for channel in result['pinned_peers'] + result['include_peers']:
        try:

            channel_id = int(channel['channel_id'])
            my_channel = await client.get_entity(types.PeerChannel(channel_id))

            async with client.action(my_channel, 'typing'):
                await client.send_message(my_channel, message=message)
            await asyncio.sleep(1)
            global count
            count += 1
            # ch = client.get_entity(channel_id)
            # print(f'sent to {my_channel.title}')

        except KeyError:
            continue
        except errors.rpcbaseerrors.ForbiddenError:
            print('Forbidden: ', my_channel.title)
            # print(e)
        except errors.rpcerrorlist.UserBannedInChannelError as e:
            print('Ban: ', my_channel.title)
            # client.delete_dialog(channel_id)
            print(repr(e))
            print('channel deleted')
        except errors.rpcerrorlist.ChannelPrivateError as e:
            print('Private: ', my_channel.title)
            print(e)
        except errors.rpcerrorlist.SlowModeWaitError:
            continue
        except Exception as e:
            print('Error: ', my_channel.title)
            print(repr(e))


# time.sleep(10 * 60)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    for current_client in clients:
        with current_client as client:
            client.session.save_entities = False
            client.loop.run_until_complete(main())
