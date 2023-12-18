import config
from telethon.sync import TelegramClient

client1 = TelegramClient("tools1", config.api_id, config.api_hash)
client2 = TelegramClient("tools2", config.api_id2, config.api_hash2)
client3 = TelegramClient("tools3", config.api_id2, config.api_hash2)
clients = [client1, client2, client3]


def show_client(client):
    if client == client1:
        return "client1"
    elif client == client2:
        return "client2"
    else:
        return "client3"
