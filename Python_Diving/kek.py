import requests

response = requests.get("https://vk.com/mizerli26")

print(response.content)