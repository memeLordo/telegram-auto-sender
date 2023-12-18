# import json
import asyncio

from config.messages import Ads, Keywords

from loguru import logger
from telethon import errors, functions
from telethon.tl import types

from .clients import choose_clients, clients


logger.add(
    "ads_main.log",
    format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="10 MB",
    retention="2 days",
    compression="zip",
)


count = 0


@logger.catch
async def start():
    request = await client(functions.messages.GetDialogFiltersRequest())

    await send_to_channels(request)

    if client != clients[-1]:
        logger.debug(f"Current count: {count}")
        logger.success("Start waiting")
        await asyncio.sleep(10 * 60)

    # async for dialog in client.iter_dialogs():
    #     logger.info(dialog.id)
    #     logger.info(client.get_entity(GetFullChannel(dialog.id)))
    # if dialog.id in ad_channels_1:
    #     logger.info('success')
    # if dialog.name == 'Golubin | Assistant':
    #     logger.info(dialog.id)
    # await send_to_channels(SEARCHED_DIRS)


# @logger.catch
async def send_to_channels(request, dirs=Keywords.SEARCHED_DIRS):
    for dialog_filter in request:
        result = dialog_filter.to_dict()
        try:
            title = result["title"]

            if title in dirs:
                logger.info("Current dir: " + result["title"])
                #
                await asyncio.sleep(1)

                match title:
                    case "Free assist":
                        await send_message_to_channel(result, Ads.FREE_ASSIST)
                        await asyncio.sleep(3)

                    case "Новые FA":
                        await send_message_to_channel(result, Ads.NEW_FA)
                        await asyncio.sleep(3)

                    # case 'КазаньSMS':
                    #     await send_message_to_channel(result, ad_kazan)
                    #     await asyncio.sleep(3)

                logger.success("Sent!")

        except KeyError:
            pass


@logger.catch
async def send_message_to_channel(result, message):
    for channel in result["pinned_peers"] + result["include_peers"]:
        try:
            channel_id = int(channel["channel_id"])
            my_channel = await client.get_entity(types.PeerChannel(channel_id))

            async with client.action(my_channel, "typing"):
                await client.send_message(my_channel, message=message)
            await asyncio.sleep(1)
            global count
            count += 1
            logger.debug(my_channel.title)

        except KeyError:
            continue
        except errors.rpcerrorlist.SlowModeWaitError:
            continue
        except errors.rpcbaseerrors.ForbiddenError:
            logger.warning(f"Forbidden: {my_channel.title}")
            # logger.info(e)
        except errors.rpcerrorlist.UserBannedInChannelError:
            logger.error(f"Ban: {my_channel.title}")
            await client.delete_dialog(my_channel)
            # logger.info(repr(e))
            logger.info("channel deleted")
        except errors.rpcerrorlist.ChannelPrivateError:
            logger.warning(f"Private: {my_channel.title}")
            # logger.info(repr(e))

        # except Exception as e:
        #     logger.info('Error: ', my_channel.title)
        #     logger.info(repr(e))

    # loop = asyncio.get_event_loop()


if __name__ == "__main__":
    try:
        clients = choose_clients(clients)
        for current_client in clients:
            with current_client as client:
                client.session.save_entities = False
                client.loop.run_until_complete(start())
        logger.success(f"Total count: {count}")
    except KeyboardInterrupt:
        pass
