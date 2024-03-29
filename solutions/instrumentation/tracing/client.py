import logging
from os import getenv
from time import sleep
from requests import get

from ot import setup_tracer_provider
from opentelemetry import trace
from opentelemetry.propagate import inject


server = getenv('FIB_HOSTNAME', 'localhost')
port = getenv('FIB_PORT', 8080)
logging.basicConfig(level=logging.INFO)


def get_fib(number):
    with trace.get_tracer_provider().get_tracer(__name__).start_as_current_span("get-fib"):
        headers = {}
        inject(headers)

        logging.info(headers)

        response = get(
            "http://{}:{}/{}".format(server, port, number),
            headers=headers,
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            return None


if __name__ == "__main__":
    setup_tracer_provider()

    while True:
        for i in range(-1, 32):
            result = get_fib(i)
            print("Fibonacci of {} is {}".format(i, result))
            sleep(1)
