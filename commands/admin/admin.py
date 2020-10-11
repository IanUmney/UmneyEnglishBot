from utils import vault

def secretary(command):
    data = vault.get_data()
    return_message = None

    if command == "list":
        return_message = "key - Generate a premium key\nstats - show statistics for all bots"
    elif command == "key":
        return_message = key = vault.create_license_key()
    elif command == 'stats':
        active_channels = len(data['channels'])
        member_count = 0
        for channel in data['channels']:
            member_count += data['channels'][channel]['member_count']
        oed_searches = data['admin']['stats']['oed_searches']
        return f'There are <b>{active_channels}</b> active channels with <b>{member_count}</b> total members .\nThere has been <b>{oed_searches}</b> searches of the OED.'
    else:
        return_message = "Invalid command!"

    return return_message
