import argparse
import json
import tempfile
import os

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

parser = argparse.ArgumentParser()
parser.add_argument("--key", help = 'insert key')
parser.add_argument("--val")
args = parser.parse_args()

#print(args.key, args.val)

key = args.key
value = args.val

def get_dict():
    if not os.path.exists(storage_path):
        return {}
    else:
        with open(storage_path, 'r') as f:
            raw_dict = f.read()
            if raw_dict:
                return json.loads(raw_dict)
            else:
                return {}

def put(key, value):
    dictionary = get_dict()
    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]

    with open(storage_path, 'w') as f:
        f.write(json.dumps(dictionary))

def get(key):
    dictionary = get_dict()

    return dictionary.get(key)

if key and value:
    put(key, value)
elif key:
    res = get(key)
    if res:
        print(', '.join(res))
    else:
        print('')
else:
    print("Wrong command")