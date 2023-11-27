import json
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.sessions import StringSession
import config

# Use your own values from my.telegram.org


# # The first parameter is the .session file name (absolute paths allowed)
# with TelegramClient('anon', api_id, api_hash) as client:
#     client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
client = TelegramClient('lol', config.api_id2, config.api_hash2)
SEARCHED_DIRS = ['Новые FA','Free assist']

async def main():
    request = await client(functions.messages.GetDialogFiltersRequest())
    for dialog_filter in request:
        result = dialog_filter.to_dict()
        try:

            if(result['title'] in SEARCHED_DIRS):
                print(result['title'])
                
                for channel in result['pinned_peers']:
                    try:
                        print(channel['channel_id'])
                    except KeyError:
                        pass

                for channel in result['include_peers']:
                    try:
                        print(channel['channel_id'])
                    except KeyError:
                        pass
        except KeyError:
           pass 
        # if(dialog_filter.to_dict()[0]=='Новые FA'):
        #     print('ok!')
        # print(dialog_filter.to_dict())
        # print(json.dumps(result))

with client:
    client.session.save_entities = False
    client.loop.run_until_complete(main())
