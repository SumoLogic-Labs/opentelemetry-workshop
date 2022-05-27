# OpenTelemetry Workshop

## What is OpenTelemetry

Short presentation on what is OpenTelemetry in general, what it can be used for: [Observability 2.0 vs OpenTelemetry](https://slides.com/perk/obsevability-20-feat-opentelemetry)

## Data creation

* Manual instrumentation: write a simple application which creates logs, metrics and traces using the OpenTelemetry libraries

* Autoinstrumentation: Pet Clinic

## Data collection

### OpenTelemetry Collector Distributions

* [Core and contrib](./exercises/distros/otelcol-and-contrib/)
* [Custom / vendor provided](./exercises/distros/custom/)

### Basic configuration

* Basics
* Extensions
* Telemetry
* Environment variables

### Receivers

* Logs, metrics and traces
  * [OTLP](./exercises/receivers/otlp/)

* Logs
  * [Filelog](./exercises/receivers/filelog/)
    * operator - router
    * multiline logs
  * [Syslog](./exercises/receivers/syslog/)

* Metrics
  * [Host Metrics](./exercises/receivers/hostmetrics/)
  * [Docker Stats](./exercises/receivers/dockerstats/)
  * [Simple Prometheus](./exercises/receivers/simpleprometheus/)
  * [Redis](./exercises/receivers/redisreceiver/)

* Traces
  * Jaeger, Zipkin


### Processors

* [Memory Limiter](./exercises/processors/memorylimiter/)
* [Filter](./exercises/processors/filter/)
* [Resource Detection](./exercises/processors/resourcedetection/)
* [Resource](./exercises/processors/resource/)
* [Attributes](./exercises/processors/attributes/)
* [Metrics Transform](./exercises/processors/metricstransform/)
* [Transform](./exercises/processors/transform/)

### Exporters
  
* File
* OTLP
* Load balancing
* [Prometheus](./exercises/exporters/prometheus/)
* Sumo Logic

## The Coffee Bar app
