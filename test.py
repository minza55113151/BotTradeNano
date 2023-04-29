from binance import Client
from time import time

API_KEY = "GRJaQlXdXyjHzKJv6uyfxIO1z7mTqq4QFzF0yFt4REJS1krN9lN2QipoDjfAg9lE"
SECRET_KEY = "J6rVvqYmHcSnQ6feekOxetR7WnCVGbDSt7qwzjJoUyMuBE6gpmb6Gb6Q6E9gfj7v"

t0 = time()
for i in range(1):
    client = Client(API_KEY, SECRET_KEY, testnet=True)
t1 = time()

print(f"Time to create client: {t1-t0} seconds")