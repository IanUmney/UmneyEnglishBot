import json
from utils import vault


def is_premium(chat_id):
    data = vaut.get_data()
    if data['channels'][chat_id]['premium']:
        return True

def remove_channel(chat_id):
    data = vault.get_data()
    del data['channels'][str(chat_id)]
    vault.dump_data(data)

def add_channel(message, online, member_count):
    data = vault.get_data()

    chat_id = str(message.chat.id)
    channel_title = message.chat.title
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    if chat_id in data['channels']:return
    if message.chat.id == message.from_user.id:
        premium = True
    else:
        premium = False
    if message.chat.id == message.from_user.id:
        oed_searches = 250
    else:
        oed_searches = 60
    data['channels'][chat_id] = {}
    data['channels'][chat_id]['member_count'] = member_count-1
    data['channels'][chat_id]['premium'] = premium
    data['channels'][chat_id]['channel_title'] = channel_title
    data['channels'][chat_id]['joined_by_id'] = user_id
    data['channels'][chat_id]['joined_by'] = user_name
    data['channels'][chat_id]['online'] = online
    data['channels'][chat_id]['oed_searches'] = oed_searches
    data['channels'][chat_id]['zoom'] = {}
    data['channels'][chat_id]['vocabulary'] = {}
    data['channels'][chat_id]['teachers'] = {}

    vault.dump_data(data)


def upgrade_channel(chat_id, key_used):
    data = vault.get_data()
    if key_used in data['admin']['keys_outstanding']:
        data['channels'][chat_id]['premium'] = True
        data['channels'][chat_id]['oed_searches'] = 250
        data['channels'][chat_id]['key_used'] = key_used
        data['admin']["keys_outstanding"].remove(key_used)
        vault.dump_data(data)
        return("You are now upgraded")
    else:
        return ("That key is invalid")
