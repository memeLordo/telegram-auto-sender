import config
from telethon.sync import TelegramClient

client1 = TelegramClient("tools1", config.api_id, config.api_hash)
client2 = TelegramClient("tools2", config.api_id2, config.api_hash2)
client3 = TelegramClient("tools3", config.api_id2, config.api_hash2)
clients = [client1, client2, client3]


show_client = {client1: "client1", client2: "client2", client3: "client3"}
