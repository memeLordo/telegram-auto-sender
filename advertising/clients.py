import sys

import config
from telethon.sync import TelegramClient

clients = [
    TelegramClient("session1", config.api_id, config.api_hash),
    TelegramClient("session2", config.api_id2, config.api_hash2),
    TelegramClient("session3", config.api_id2, config.api_hash2),
]


def choose_clients(client_list=clients):
    key_clients = sys.argv[1: 3 + 1]
    if not key_clients:
        return client_list
    return list(client_list[int(x) - 1] for x in key_clients)
