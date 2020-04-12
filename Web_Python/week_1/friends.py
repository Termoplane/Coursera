import requests

ACCESS_TOKEN = '44988aec44988aec44988aecfb44e8261d4449844988aec1a1bd3cfeade0c597975fbb0'

def get_id(username):
    user_data = requests.get(f'https://api.vk.com/method/users.get?v=5.71&access_token={ACCESS_TOKEN}&user_ids={username}')
    user_data = user_data.json()
    user_id = user_data['response'][0]['id']
    return user_id

def get_friends(user_id):
    user_friends = requests.get(f'https://api.vk.com/method/friends.get?v=5.71&access_token={ACCESS_TOKEN}&user_id={user_id}&fields=bdate')
    user_friends = user_friends.json()
    user_friends = user_friends['response']['items']
    return user_friends


def calc_age(username):
    ages = {}
    user_id = get_id(username)
    user_friends = get_friends(user_id)

    for friend in user_friends:
        friend_bdate = friend.get('bdate')
        if not friend_bdate:
            continue
        
        bdate = friend_bdate.split('.')

        if len(bdate) != 3:
            continue

        year = 2020 - int(bdate[2])

        if year in ages: 
            ages[year] += 1
        else:
            ages[year] = 1
        
    return sorted(ages.items(), key=lambda v: (-v[1], v[0]))





if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)