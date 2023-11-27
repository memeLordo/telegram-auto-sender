from telethon import TelegramClient

# Use your own values from my.telegram.org
api_id = 25065727
api_hash = '3a71d090e43792526725d63bef945ce3'

# # The first parameter is the .session file name (absolute paths allowed)
# with TelegramClient('anon', api_id, api_hash) as client:
#     client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
client = TelegramClient('anon', api_id, api_hash)

async def main():
    # Getting information about yourself
    me = await client.get_me()
    print(me.stringify())
    username = me.username
    print(username)
    print(me.phone)

with client:
    client.loop.run_until_complete(main())
