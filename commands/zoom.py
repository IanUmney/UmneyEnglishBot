import json
from utils import vault

data = vault.get_data()

def zoom_exists(chat_id):
    if bool(data['channels'][str(chat_id)]['zoom']):
        return True
    else:
        return False

def add_link(chat_id, name, link):
    data['channels'][chat_id]['zoom'][name] = link
    vault.dump_data(data)
    return f'{name}\'s zoom link has been added'

def delete_link(chat_id, name):
    if zoom_exists(chat_id):
        if name in data['channels'][chat_id]['zoom']:
            del data['channels'][chat_id]['zoom'][name]
            vault.dump_data(data)
            return f'{name}\'s zoom link has been deleted'
        else:
            return f'There is no record of {name} in the database'

def get_group_links(chat_id):
    if zoom_exists(chat_id):
        group_list = ''
        for name in data['channels'][chat_id]['zoom']:
            link = f"{name}: {data['channels'][chat_id]['zoom'][name]}\n"
            group_list += link
        if len(group_list) >= 1:
            return group_list
    else:
        return f'Your group does not have any zoom links'

def get_teacher_link(chat_id, name):
    if zoom_exists(chat_id):
        if name in data['channels'][chat_id]['zoom']:
            return f"{name}: {data['channels'][chat_id]['zoom'][name]}"
    else:
        return f'{name} not found in the database'
