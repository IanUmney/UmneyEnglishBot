from utils import vault

data = vault.get_data()

def list_all(chat_id):
    list = ''
    if bool(data['channels'][chat_id]['vocabulary']):
        for topic in data['channels'][chat_id]['vocabulary']:
            list += f'{topic}\n'
        return '<b>The topics in your vocabulary list are:</b>\n\n' + list
    else:
        return "There are no vocabulary lists.\nUse /vocab [topic] [words]"

def list_individual(chat_id, list_name):
    try:
        list = f'<b>{list_name}</b>\n\n'
        if bool(data['channels'][chat_id]['vocabulary'][list_name]):
            for item in data['channels'][chat_id]['vocabulary'][list_name]:
                list += f'{item}\n'
            return list
    except:
        return f'"{list_name}" does not exist in your vocabulary list. Use /vocab to see all lists.'

def delete_list(chat_id, list_name):
    del data['channels'][chat_id]['vocabulary'][list_name]
    vault.dump_data(data)
    return f'Deleted "{list_name}" vocabulary list.'

def add_list(chat_id, topic, words):
    try:
        if bool(data['channels'][chat_id]['vocabulary'][topic]):
            wordlist = ''
            for x in words:
                data['channels'][chat_id]['vocabulary'][topic].append(x)
                vault.dump_data(data)
                wordlist += f'"{x}" '
            return f'Added {wordlist}to the "{topic}" vocab list.'
    except:
        data['channels'][str(chat_id)]['vocabulary'][topic] = words
        vault.dump_data(data)
        return f'Added the vocabulary list "{topic}"'
