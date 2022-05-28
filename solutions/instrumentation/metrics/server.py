import logging
from flask import Flask

from ot import setup_metric_provider

from opentelemetry._metrics import get_meter_provider

app = Flask(__name__)


@app.route("/")
def info():
    return '''<html><body>
    Welcome to Fibonacci calculation microservice!
    
    Example usage:
    
    <pre>
    $ curl http://localhost:8080/6
    
    {"argument":5,"result":8}
    </pre>
    
    It is a modest service for modest Fibonacci numbers calculation
    </body></html>
    '''


@app.route("/<number>")
def number_request(number):
    request_counter.add(1)

    try:
        parsed_number = int(number)

        return {
            "argument": parsed_number,
            "result": fibonacci(parsed_number)
        }
    except ValueError as err:
        failure_counter.add(1)
        logging.exception(err)
        return 'Invalid request', 400


def fibonacci(n):
    if n < 0:
        raise ValueError('Negative value not supported')
    if n > 35:
        raise ValueError('Value too large')
    if n in {0, 1}:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


setup_metric_provider()

meter = get_meter_provider().get_meter("workshop", "0.1")
request_counter = meter.create_counter("requests_count")
failure_counter = meter.create_counter("failed_requests_count")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
