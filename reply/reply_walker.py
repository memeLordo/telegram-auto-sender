import asyncio

from config.messages import Keywords, Reply
from loguru import logger
from tools.editor import remove_punct

from .clients import clients, show_client

logger.add(
    "process.log",
    format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="2 days",
    compression="zip",
)


@logger.catch
async def sent_reply_start(client, bebra, error_exit=False):
    log_name = bebra.first_name
    first_name = bebra.first_name.split(" ")[0]
    sender = bebra.username
    if not error_exit:
        logger.info(f"{show_client(client)}: got message from {log_name}")

    await asyncio.sleep(1)

    #############
    try:
        await client.send_read_acknowledge(sender)
        async with client.action(bebra, "typing"):
            await asyncio.sleep(4)
            await client.send_message(bebra, Reply.say_hi(first_name))

        async with client.action(bebra, "typing"):
            await asyncio.sleep(5)
            await client.send_message(sender, Reply.FORM)
            logger.debug(f"{show_client(client)}: message sent to {log_name}")

    except ValueError:
        logger.error(f"{show_client(client)}: {log_name} is unknown")

        if error_exit:
            raise ValueError(f"{show_client(client)}: Still unresolved")

        dialogs = client.iter_dialogs()
        async for dialog in dialogs:
            try:
                if dialog.entity.id == bebra.id:
                    logger.info(f"{log_name}'s ID found")
                    bebra = dialog.entity
                    # logger.debug(bebra)
                    await sent_reply_start(client, bebra, True)
                    break
            except Exception as e:
                logger.critical(repr(e))


@logger.catch
async def sent_reply(client, bebra, message, error_exit=False):
    log_name = bebra.first_name
    sender = bebra.username
    logger.info(f"{show_client(client)}: got message from {log_name}")
    await asyncio.sleep(1)

    try:
        await client.send_read_acknowledge(sender)

        async with client.action(bebra.username, "typing"):
            await asyncio.sleep(4)
            await client.send_message(sender, message)
            logger.debug(f"{show_client(client)}: message sent to {log_name}")
    except ValueError:
        logger.error(f"{show_client(client)}: {log_name} is unknown")

        if error_exit:
            raise ValueError(f"{show_client(client)}: Still unresolved")

        dialogs = client.iter_dialogs()
        async for dialog in dialogs:
            try:
                if dialog.entity.id == bebra.id:
                    logger.info(f"{log_name}'s ID found")
                    bebra = dialog.entity
                    # logger.debug(bebra)
                    await sent_reply(client, bebra, message, True)
                    break
            except Exception as e:
                logger.critical(repr(e))


async def match_sent_message(client, user, message):
    # logger.opt(colors=True).debug(f"<white>{message}</white>")
    r_message = set(remove_punct(message).split(" "))
    key = set(Keywords.FIRST_MESSAGE)
    if key & r_message:
        await sent_reply_start(client, user)
    upprove = Keywords.FIRST_MESSAGE
    ignore = Keywords.IGNORE


@logger.catch
async def check_new_messages():
    await client.start()
    dialogs = client.iter_dialogs()

    async for dialog in dialogs:
        try:
            bebra = dialog.entity
            message = str(dialog.message.message).lower()

            await match_sent_message(client, bebra, message)
        except ValueError as e:
            logger.critical(e.__class__.__name__)
            # print(dialog.name)
    logger.debug(show_client(client))


@logger.catch
def run_message_checker():
    logger.info("Begin check")
    for current_client in clients:
        global client
        with current_client as client:
            client.session.save_entities = False
            client.loop.run_until_complete(check_new_messages())
    logger.success("")


if __name__ == "__main__":
    try:
        run_message_checker()
        # start_event_handler()
    except KeyboardInterrupt:
        pass
