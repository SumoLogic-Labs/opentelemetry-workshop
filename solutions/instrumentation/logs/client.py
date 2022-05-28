from os import getenv
from time import sleep
from requests import get

from ot import setup_log_provider


server = getenv('FIB_HOSTNAME', 'localhost')
port = getenv('FIB_PORT', 8080)


def get_fib(number):
    response = get(
        "http://{}:{}/{}".format(server, port, number),
    )

    if response.status_code == 200:
        return response.json()['result']
    else:
        return None


if __name__ == "__main__":
    setup_log_provider()

    while True:
        for i in range(-1, 32):
            result = get_fib(i)
            print("Fibonacci of {} is {}".format(i, result))
            sleep(1)
