import sys
from datetime import datetime

import config

from loguru import logger
from telethon import types
from telethon.sync import TelegramClient

logger.remove()
logger.add(sys.stderr, level="DEBUG")

client1 = TelegramClient('count1', config.api_id, config.api_hash)
client2 = TelegramClient('count2', config.api_id2, config.api_hash2)
client3 = TelegramClient('count3', config.api_id2, config.api_hash2)
clients = [client1, client2, client3]


def show_client(client):
    if client == client1:
        return 'client1'
    elif client == client2:
        return 'client2'
    else:
        return 'client3'


@logger.catch
async def start():
    logger.warning(f'Counting in {show_client(client)}')

    await count_users()
    if client != clients[-1]:
        logger.debug(f'Current count: {count}')


async def exclude_users():
    dialogs = await client.get_dialogs(archived=False)
    users = list(filter(lambda x: isinstance(x.entity, types.User), dialogs))
    logger.info(f'Exclude users succses! {len(users)}')
    return users


async def bebra_wrapper(user, data):
    client_messages = await client.get_messages(entity=user,
                                                reverse=True,
                                                limit=1,
                                                from_user=user)
    if not (client_messages and client_messages.total < 30):
        return
    data.append(client_messages)
    logger.trace(client_messages.total)


async def count_users():
    users = await exclude_users()
    messages_data = []
    for bebra in users:
        await client.loop.create_task(
            bebra_wrapper(bebra.entity, messages_data))

    for date in todate:
        input_date = datetime.strptime(date, '%d.%m.%y').date()
        count[date] += len(
            list(
                filter(lambda x: x[0].date.date() == input_date,
                       messages_data)))


def choose_date():
    input_date = sys.argv[1:]
    today = [datetime.today().strftime('%d.%m.%y')]
    if not input_date:
        return today
    return list(x for x in input_date)


if __name__ == '__main__':
    global todate, count
    todate = choose_date()
    count = dict.fromkeys(todate, 0)
    logger.trace(count)

    for current_client in clients:
        with current_client as client:
            client.session.save_entities = False
            client.loop.run_until_complete(start())
    for key, value in count.items():
        print(f'{key}\t{value}')
