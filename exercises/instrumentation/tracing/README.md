# OpenTelemetry tracing instrumentation

Tracing allows to observe the cycle of a distributed transaction and how it goes through
all of the affected services. In essence, Trace is a DAG (Direct Acyclic Graph) built from
Spans. Each Span defines a segment of operation in a given service.

To make that possible, services need to exchange [context](https://opentelemetry.io/docs/concepts/otel-concepts/#span-context) with each request. This is done
by a mechanism named as [context propagation](https://opentelemetry.io/docs/reference/specification/context/context/).
Most commonly, [w3c trace context](https://www.w3.org/TR/trace-context/) is being used for the purpose.
The trace-id and parent-span-id are passwed with each request, which allows to continue the trace.

In this exercise we will observe that mechanism and see how to create and enrich spans.

## Setting up the libraries

The directory already includes required libraries in [requirements.txt](requirements.txt) and contains
the intialization routines in [ot.py](ot.py). Please review those. This can be also simplified
by using [OpenTelemetry Python Distro](https://opentelemetry.io/docs/instrumentation/python/distro/)

The docker-compose file also includes the OTLP exporter setup.

We also included zipkin backend. This will allow us to investigate the traces later on.

## Initialization

At first, we need to initialize the trace provider

```python
setup_tracer_provider()
```

Please make sure that imports are also included:
```python
from ot import setup_tracer_provider
```

The step needs to be reproduced for both `client` and `server`

## Instrumenting the request

We start with client, in which we are going to get the global tracer provider
and start new span with operation `get-fib`. To propagate the context,
we need to inject the headers, i.e. 

```python
from opentelemetry import trace
from opentelemetry.propagate import inject
```

```python
with trace.get_tracer_provider().get_tracer(__name__).start_as_current_span("get-fib"):
    headers = {}
    inject(headers)

    response = get(
        "http://{}:{}/{}".format(server, port, number),
        headers=headers,
    )
```
### What is in the headers?

If you are curious, check the content of headers, e.g. by simple `print(headers)`.

## Instrumenting the server

Now we need to do a similar operation on the server side, starting with imports.

```python
from opentelemetry import trace
from opentelemetry.trace.status import StatusCode
from opentelemetry.instrumentation.wsgi import collect_request_attributes
from opentelemetry.propagate import extract
```
Here, we create a new span named `number_request`. We identify its kind to be `SERVER` and
extract the headers, which will allow us to retrieve the context. Additionally, we collect
additional HTTP request attributes via `collect_request_attributes` helper.
```python
with trace.get_tracer(__name__).start_as_current_span(
    "number_request",
    context=extract(request.headers),
    kind=trace.SpanKind.SERVER,
    attributes=collect_request_attributes(request.environ),
) as span:
```

At this stage, the example is already functional. Let's extend it a bit though.

## Collecting additional attributes

We can easily attach more attributes to the current span via `set_attribute`, for example:
```python
span.set_attribute("number", parsed_number)
```

## Recording error status

Lets extend the `except` block with capturing the cause of the error and marking the status
accordingly:

```python
span.record_exception(err)
```

## Running

Having all of that, lets run the setup
```
docker-compose build && docker-compose up
```

The spans should be logged by OpenTelemetry Collector logging exporter. Additionally, those
should be sent to the OpenZipkin backend, which allows to see them at 
[http://localhost:9411](http://localhost:9411)

## Sampling

To reduce the volume of data, sampling can be used. Sampling parameters can be passed using SDK environment
variables. For example:

```
- OTEL_TRACES_SAMPLER=traceidratio
- OTEL_TRACES_SAMPLER_ARG=0.1
```