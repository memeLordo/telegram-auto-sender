import sys
from typing import List

import config
from telethon.sync import TelegramClient


client1 = TelegramClient("session1", config.api_id, config.api_hash)
client2 = TelegramClient("session2", config.api_id2, config.api_hash2)
client3 = TelegramClient("session3", config.api_id2, config.api_hash2)

clients = [client1, client2, client3]


def choose_clients(client_list: List[TelegramClient] = clients) -> list:
    key_clients: list = sys.argv[1: 3 + 1]
    if not key_clients:
        return client_list
    return list(client_list[int(x) - 1] for x in key_clients)


show_client = {client1: "client1", client2: "client2", client3: "client3"}
