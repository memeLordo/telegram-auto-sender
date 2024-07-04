import sys
from datetime import date, datetime
from typing import List

from loguru import logger
from telethon.types import User

from .checker import is_user
from .clients import clients, show_client

logger.remove()
logger.add(sys.stderr, level="DEBUG")


@logger.catch
async def start() -> None:
    logger.warning(f"Counting in {show_client[client]}")

    await count_users()
    if client != clients[-1]:
        logger.debug(f"Current count: {count}")


async def exclude_users() -> List[User]:
    dialogs = await client.get_dialogs(archived=False)
    users = list(filter(lambda x: is_user(x.entity), dialogs))
    logger.info(f"Exclude users succses! {len(users)}")
    return users


async def bebra_wrapper(user: User, data: List[User]) -> None:
    client_messages = await client.get_messages(
        entity=user, reverse=True, limit=1, from_user=user
    )
    if not (client_messages and client_messages.total < 30):
        return
    data.append(client_messages)
    logger.trace(client_messages.total)


async def count_users() -> None:
    users = await exclude_users()
    msg_data = []
    for bebra in users:
        await client.loop.create_task(bebra_wrapper(bebra.entity, msg_data))

    for _date in todate:
        try:
            inpt_date = datetime.strptime(_date, "%d.%m.%y").date()
            count[_date] += len(
                list(filter(lambda x: x[0].date.date() == inpt_date, msg_data))
            )
        except ValueError:
            continue


def choose_date() -> date:
    input_date: list = sys.argv[1:]
    today = [datetime.today().strftime("%d.%m.%y")]
    if not input_date:
        return today
    return list(x for x in input_date)


if __name__ == "__main__":
    global todate, count
    try:
        todate = choose_date()
        count = dict.fromkeys(todate, 0)
        logger.trace(count)

        for current_client in clients:
            global client
            with current_client as client:
                client.session.save_entities = False
                client.loop.run_until_complete(start())
        for key, value in count.items():
            print(f"{key} {value}")
    except KeyboardInterrupt:
        pass
