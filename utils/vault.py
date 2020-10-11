import hashlib, random, string, json

def encode_string_to_byte(string):
    return string.encode()
def encrypt(string):
    return hashlib.sha256(encode_string_to_byte(string)).hexdigest()


def create_license_keys(number):
    x = int(number)
    list = []
    while x > 0:
        key = create_license_key()
        # print(key)
        list.append(key)
        x -= 1
    return list

def create_license_key():
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    data = get_data()
    data["admin"]["keys_outstanding"].append(key)
    dump_data(data)
    return key

def get_data():
    with open("lib/data.json", "r") as json_file:
        data = json.load(json_file)
    return data


def dump_data(data):
    with open("lib/data.json", "w") as file_json:
        json.dump(data, file_json, indent=4)

def create_license_key():
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    data = get_data()
    data["admin"]["keys_outstanding"].append(key)
    dump_data(data)
    return key
