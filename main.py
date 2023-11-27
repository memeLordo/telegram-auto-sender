import json
from telethon import TelegramClient, functions
from telethon.sessions import StringSession

# Use your own values from my.telegram.org
api_id = 25065727
api_hash = '3a71d090e43792526725d63bef945ce3'

# # The first parameter is the .session file name (absolute paths allowed)
# with TelegramClient('anon', api_id, api_hash) as client:
#     client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
client = TelegramClient('lol', api_id, api_hash)

async def main():
    request = await client(functions.messages.GetDialogFiltersRequest())
    for dialog_filter in request:
        print(json.dumps(dialog_filter.to_dict()))

with client:
    client.loop.run_until_complete(main())
