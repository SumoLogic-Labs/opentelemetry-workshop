# OpenTelemetry Metrics instrumentation

For this exercise, we will simplify a couple of things. Since you are already aware on the pipeline setup, we
are going to use one that is readily available.

OpenTelemetry supports [several kinds of instruments](https://opentelemetry-python.readthedocs.io/en/stable/api/metrics.html),
which are accessible through [the SDK](https://opentelemetry-python.readthedocs.io/en/stable/sdk/metrics.html)

For the purpose of this exercise we will just play with the counters, but we encourage you to play
with other types as well.

## Setting up the libraries

The directory already includes required libraries in [requirements.txt](requirements.txt) and contains
the intialization routines in [ot.py](ot.py). Please review those.

The docker-compose file also includes the OTLP exporter setup.

## Adding the instruments

At first, we need to create the meter provider instance and attach two counter instruments.
We are going to count requests (of all kinds) and failed ones separately

```python
setup_metric_provider()

meter = get_meter_provider().get_meter("workshop", "0.1")
request_counter = meter.create_counter("requests_count")
failure_counter = meter.create_counter("failed_requests_count")
```

Please make sure that imports are also included:
```python
from ot import setup_metric_provider

from opentelemetry._metrics import get_meter_provider
```

## Measuring

Add measurements of successful and failed requests by referring the counter and calling
the add function. E.g.

```python
request_counter.add(1)
```

## Running

Having all steps done, please run the new service, e.g.

```
docker-compose build && docker-compose up
```

You should observe that OpenTelemetry Collector actually receives the messages and puts
them on the console, including all the attributes

## Taking it further

You can play around and add more types of instruments (histograms, gauges, etc.)

