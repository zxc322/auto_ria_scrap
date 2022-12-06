URL = "https://auto.ria.com/uk/car/used/"
PHONE_URL = "https://auto.ria.com/users/phones/" # GET
PHONE_URL_V2 = "https://auto.ria.com/newauto/api/auth/dc" # POST

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62',
    'Content-Type': 'application/json;charset=UTF-8',
    'accept-language': 'en-US,en;q=0.9',
    'accept': '*/*',
    'cache-control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br',
    'authority': 'auto.ria.com',
    'Connection': 'keep-alive'
}

data = {"adv_id":1895425,"phone_id":"680971717","platform":"desktop"}