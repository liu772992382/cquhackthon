import requests

url = "https://www.yiban.cn/user/index/index/user_id/5297459"

headers = {
    'cache-control': "no-cache",
    'postman-token': "b465d87b-512e-b697-b782-1cbe0ec33e38"
    }

response = requests.request("GET", url, headers=headers)

print response.cookies
