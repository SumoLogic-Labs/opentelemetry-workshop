# OpenTelemetry Workshop

## What is OpenTelemetry

Short presentation on OpenTelemetry in general: [Observability 2.0 vs OpenTelemetry](https://slides.com/perk/obsevability-20-feat-opentelemetry)

## Data creation

* [Manual instrumentation](./exercises/instrumentation/): write a simple application which creates logs, metrics and traces using the OpenTelemetry libraries

* For autoinstrumentation please take a look at [Spring PetClinic](https://github.com/SumoLogic/opentelemetry-petclinic) demo at the end of the workshop

## Data collection

### OpenTelemetry Collector Distributions

* [Core and contrib](./exercises/distros/otelcol-and-contrib/)
* [Custom / vendor provided](./exercises/distros/custom/)

### Configuration basics

#### Basics

* [Basics](https://opentelemetry.io/docs/collector/configuration/#basics)
* [Receivers](https://opentelemetry.io/docs/collector/configuration/#receivers)
* [Processors](https://opentelemetry.io/docs/collector/configuration/#processors)
* [Exporters](https://opentelemetry.io/docs/collector/configuration/#exporters)
* [Extensions](https://opentelemetry.io/docs/collector/configuration/#extensions)
* [Service](https://opentelemetry.io/docs/collector/configuration/#service)
* [Telemetry](./exercises/basics/telemetry/)
* [Environment variables](./exercises/basics/env-variables/)

#### Extensions

* [Health Check](./exercises/extensions/healthcheck/)
* [zPages](./exercises/extensions/zpages/)
* Other extensions:
  * [OpenTelemetry Collector extensions](https://github.com/open-telemetry/opentelemetry-collector/tree/v0.51.0/extension)
  * [OpenTelemetry Collector Contrib extensions](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/extension)

### Receivers

* Logs, metrics and traces
  * [OTLP](./exercises/receivers/otlp/)
* Logs
  * [Filelog](./exercises/receivers/filelog/)
  * [Syslog](./exercises/receivers/syslog/)
* Metrics
  * [Host Metrics](./exercises/receivers/hostmetrics/)
  * [Docker Stats](./exercises/receivers/dockerstats/)
  * [Simple Prometheus](./exercises/receivers/simpleprometheus/)
  * [Redis](./exercises/receivers/redisreceiver/)
* Traces
  * [Zipkin, Jaeger](./exercises/receivers/zipkin/)
* Other receivers:
  * [OpenTelemetry Collector receivers](https://github.com/open-telemetry/opentelemetry-collector/tree/v0.51.0/receiver)
  * [OpenTelemetry Collector Contrib receivers](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/receiver)

### Processors

* [Memory Limiter](./exercises/processors/memorylimiter/)
* [Filter](./exercises/processors/filter/)
* [Resource Detection](./exercises/processors/resourcedetection/)
* [Resource](./exercises/processors/resource/)
* [Attributes](./exercises/processors/attributes/)
* [Metrics Transform](./exercises/processors/metricstransform/)
* [Transform](./exercises/processors/transform/)
* [Tail Sampling](./exercises/processors/tailsampling/)
* Other processors:
  * [OpenTelemetry Collector processors](https://github.com/open-telemetry/opentelemetry-collector/tree/v0.51.0/processor)
  * [OpenTelemetry Collector Contrib processors](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/processor)

### Exporters
  
* [File](./exercises/exporters/file/)
* [OTLP](./exercises/exporters/otlp/)
* [Load balancing](./exercises/exporters/loadbalancing/)
* [Prometheus](./exercises/exporters/prometheus/)
* Other exporters:
  * [OpenTelemetry Collector exporters](https://github.com/open-telemetry/opentelemetry-collector/tree/v0.51.0/exporter)
  * [OpenTelemetry Collector Contrib exporters](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/exporter)

## Demo

* [Prerequisites](./exercises/demo/prerequisites/)
* [Sumo Logic OpenTelemetry Collector](./exercises/demo/sumologic-otel-collector/)
* [The Coffee Bar](./exercises/the-coffee-bar/)
* [Pet Clinic](https://github.com/SumoLogic/opentelemetry-petclinic)
