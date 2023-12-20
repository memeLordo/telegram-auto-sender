import sys

import config
from telethon import TelegramClient

client1 = TelegramClient("reply1", config.api_id, config.api_hash)
client2 = TelegramClient("reply2", config.api_id2, config.api_hash2)
client3 = TelegramClient("reply3", config.api_id2, config.api_hash2)

clients = [client1, client2, client3]


def choose_clients(client_list=clients):
    key_clients = sys.argv[1: 3 + 1]
    if not key_clients:
        return client_list
    return list(client_list[int(x) - 1] for x in key_clients)


def add_count(client):
    if client == client1:
        pass
    if client == client2:
        pass
    if client == client3:
        pass


def show_client(client):
    if client == client1:
        return "client1"
    elif client == client2:
        return "client2"
    else:
        return "client3"
