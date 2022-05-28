import logging
from flask import Flask, request

from ot import setup_tracer_provider

from opentelemetry import trace
from opentelemetry.trace.status import StatusCode
from opentelemetry.instrumentation.wsgi import collect_request_attributes
from opentelemetry.propagate import extract


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
    with trace.get_tracer(__name__).start_as_current_span(
        "number_request",
        context=extract(request.headers),
        kind=trace.SpanKind.SERVER,
        attributes=collect_request_attributes(request.environ),
    ) as span:
        try:
            parsed_number = int(number)
            span.set_attribute("number", parsed_number)

            return {
                "argument": parsed_number,
                "result": fibonacci(parsed_number)
            }
        except ValueError as err:
            span.record_exception(err)
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


setup_tracer_provider()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
