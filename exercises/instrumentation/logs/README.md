# OpenTelemetry Log instrumentation

[Logs support](https://opentelemetry.io/docs/reference/specification/overview/#log-signal) is 
in early phase in OpenTelemetry Instrumentation. Rather than replacing the 
existing logging libraries, OpenTelemetry helps with consuming the log data by exporting
them via OTLP as needed.

In this exercise you will setup [Python logging to send logs via OTLP](https://opentelemetry-python.readthedocs.io/en/stable/sdk/logs.html)

## Setting up the libraries

### requirements.txt update

OpenTelemetry specific libraries need to be added as dependencies. Please add following to `requirements.txt`:

```
opentelemetry_sdk==1.11.1
opentelemetry_api==1.11.1
opentelemetry-exporter-otlp-proto-grpc==1.11.1
```

### Initialization

Please create a file where you will write the initialization code (e.g. `ot.py`). The 
initialization consists out of several sections:

#### Imports

We will need several libraries, please make sure that following are imported


```python
# Obviously (:
import logging

# OpenTelmetry has several exporters for most of the signals, though for Python & Logs 
# the options are more limited. We are ging to use use gRPC/Protobuf one
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# Resource is a common object for all signal types
from opentelemetry.sdk.resources import Resource

# Here we take several of the standard API implementations
from opentelemetry.sdk._logs import (
    LogEmitterProvider,
    LoggingHandler,
    set_log_emitter_provider,
)


from opentelemetry.sdk._logs.export import (
    # The batch processor buffers the data before sending them out
    BatchLogProcessor,
    # Optionally we might add ConsoleLogExporter (useful for debugging)
    ConsoleLogExporter,
)
```

### Logging pipeline setup

Having the imports handled, lets actually setup the instrumentation pipeline

```python

# Simple control over console logging
console_enabled = False

# Here's where the actual setup happens
def setup_log_provider():
    # First, we create the emitter provider 
    log_emitter_provider = LogEmitterProvider()
    # Globally set the log emitter provider
    set_log_emitter_provider(log_emitter_provider)

    # Add BatchLogProcessor which will buffer the records and export them using gRPC/Protobuf
    log_emitter_provider.add_log_processor(BatchLogProcessor(OTLPLogExporter()))
    if console_enabled:
        # Optionally add console output
        log_emitter_provider.add_log_processor(BatchLogProcessor(ConsoleLogExporter()))

    # Setup the basic logging (i.e. simple/native console output)
    logging.basicConfig(level=logging.DEBUG)

    # Get the emitter instance with a given name
    log_emitter = log_emitter_provider.get_log_emitter(__name__, "0.1")
    # Create a new handler which is using the specified emitter
    handler = LoggingHandler(level=logging.WARN, log_emitter=log_emitter)
    # Attach it
    logging.getLogger().addHandler(handler)
```

### Actual initialization

With the above implemented, it's not just a matter of importing the function and calling it, e.g.

```python
from ot import setup_log_provider
```

```python
setup_log_provider()
```

This shuold ideally be done in both client and the server.

## Configuring the endpoint via env variable

Please add folowing environment variable entry to docker-compose for client and server

```
- OTEL_EXPORTER_OTLP_ENDPOINT=http://otelcol:4317
```

## Configuring the service name

To identify the service a special resource-level attribute - `service.name` is used.
It can be provided in a number of ways, though perhaps the easiest is through an 
environment variable, which will be then picked by the SDK. Please fill 
the service name for client and server (using different values). E.g.:

```
- OTEL_SERVICE_NAME=some-service-name
```

The full list of environment variables supported by SDKs is available in the specification repo:
[sdk-environment-variables](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/sdk-environment-variables.md)

## Running

Having all steps done, please run the new service, e.g.

```
docker-compose build && docker-compose up
```

You should observe that OpenTelemetry Collector actually receives the messages and puts
them on the console, including all the attributes

## Playing around

Feel free to change some of the settings 

```python
handler = LoggingHandler(level=logging.INFO, log_emitter=log_emitter)
```

or add more logging messages. E.g.

```python
logging.info("I prefer Bash over Python")
```