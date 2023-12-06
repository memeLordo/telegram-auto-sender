import sys
from datetime import datetime

from loguru import logger
from telethon import functions, types
from telethon.sync import TelegramClient

import config

# from messages_config import ad_1, ad_2, ad_kazan
# from telethon.tl import types


clients = [
    TelegramClient('count1', config.api_id, config.api_hash),
    TelegramClient('count2', config.api_id2, config.api_hash2),
    TelegramClient('count3', config.api_id2, config.api_hash2),
]
SEARCHED_DIRS = ['Входящие']
count = 0


@logger.catch
async def start():
    request = await client(functions.messages.GetDialogFiltersRequest())
    await count_date(request, count)
    if client != clients[-1]:
        logger.debug(f'Current count: {count}')


async def count_date(request, count, dirs=SEARCHED_DIRS):
    for dialog_filter in request:
        result = dialog_filter.to_dict()
        try:
            title = result['title']

            if title in dirs:
                #

                match title:
                    case 'Входящие':
                        # logger.debug(result)
                        await count_users_in_dir(result, count)

                        # case 'Free assist':
                        #     await send_message_to_channel(result, ad_1)
                        #     await asyncio.sleep(3)
                        #
                        # case 'Новые FA':
                        #     await send_message_to_channel(result, ad_2)
                        #     await asyncio.sleep(3)
                        #
                        # case 'КазаньSMS':
                        #     await send_message_to_channel(result, ad_kazan)
                        #     await asyncio.sleep(3)
                        #
                logger.success('Sent!')

        except KeyError:
            pass


async def count_users_in_dir(result, count):
    data = result['pinned_peers'] + \
        result['include_peers'] + result['exclude_peers']
    for user in data:
        user_id = int(user['user_id'])
        access_hash = int(user['access_hash'])

        peer_user = types.InputPeerUser(
            user_id=user_id,
            access_hash=access_hash)

        my_user = await client.get_entity(peer_user)
        # TODO: lol

        logger.debug(my_user)


def choose_data():
    input_data = sys.argv[1:]
    global today
    today = datetime.today().strftime('%d.%m.%y')
    if not input_data:
        return today
    return list(x for x in input_data)


if __name__ == '__main__':
    # global today
    print(choose_data())

    for current_client in clients:

        with current_client as client:
            client.session.save_entities = False
            client.loop.run_until_complete(start())
    logger.success(f'Total count: {count}')
