# Load Balancing Exporter exercise

Load Balancing exporter might be very useful when spreading traces on multiple otelcol instances and thus reducing CPU load created by the Tail Sampling processor

## Run the OTLP Backend

* For this exercise we need an OTLP listening backend which will expose multiple OTLP endpoints. Let's use one `otelcol` instance for that and reffer to it as `otlp-backend`

* Run the `otlp-backend` using the [config-otlp-backend.yaml](./config-otlp-backend.yaml) file, it will:
  * listen on `0.0.0.0:14317` address for insecure OTLP/gRPC connections and forward traces to `logging` exporter
  * listen on `0.0.0.0:24317` address for insecure OTLP/gRPC connections and forward traces to `file` exporter
  * mark own service logs with the `service: otlp-backend`

  ```bash
  $ otelcol-contrib --config config-otlp-backend.yaml
  
  ...
  2022-05-29T12:46:53.648+0200	info	builder/receivers_builder.go:68	Receiver is starting...	{"service": "otlp-backend", "kind": "receiver", "name": "otlp/1"}
  2022-05-29T12:46:53.648+0200	info	otlpreceiver/otlp.go:70	Starting GRPC server on endpoint 0.0.0.0:14317	{"service": "otlp-backend", "kind": "receiver", "name": "otlp/1"}
  2022-05-29T12:46:53.649+0200	info	builder/receivers_builder.go:73	Receiver started.	{"service": "otlp-backend", "kind": "receiver", "name": "otlp/1"}
  2022-05-29T12:46:53.649+0200	info	builder/receivers_builder.go:68	Receiver is starting...	{"service": "otlp-backend", "kind": "receiver", "name": "otlp/2"}
  2022-05-29T12:46:53.649+0200	info	otlpreceiver/otlp.go:70	Starting GRPC server on endpoint 0.0.0.0:24317	{"service": "otlp-backend", "kind": "receiver", "name": "otlp/2"}
  2022-05-29T12:46:53.649+0200	info	builder/receivers_builder.go:73	Receiver started.	{"service": "otlp-backend", "kind": "receiver", "name": "otlp/2"}
  
  ...
  2022-05-29T12:46:53.649+0200	info	service/collector.go:146	Everything is ready. Begin running and processing data.	{"service": "otlp-backend"}
  ```

## Set load balancing exporter to forward data from Otelcol Agent to OTLP endpoints

* Read the [Load Balancing Exporter documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/exporter/loadbalancingexporter)

* Add the `Load Balancing exporter` to the [config.yaml](./config.yaml) file
  * remember to use insecure connection
  * keep the `logging` exporter, it will help debug problems

* In another console window, run the otelcol using updated [config](config.yaml) file - let's reffer to that instance as `otelcol-agent`:

  ```bash
  $ otelcol-contrib --config config.yaml
  
  ...
  2022-05-29T12:51:28.809+0200	info	service/service.go:81	Starting exporters...	{"service": "load-balancer"}
  2022-05-29T12:51:28.809+0200	info	builder/exporters_builder.go:40	Exporter is starting...	{"service": "load-balancer", "kind": "exporter", "name": "loadbalancing"}
  2022-05-29T12:51:28.810+0200	info	builder/exporters_builder.go:48	Exporter started.	{"service": "load-balancer", "kind": "exporter", "name": "loadbalancing"}
  
  ...
  2022-05-29T12:51:28.810+0200	info	service/collector.go:146	Everything is ready. Begin running and processing data.	{"service": "load-balancer"}
  ```

  This instance is listening on `localhost:9411` for Zipkin traces which will be fanned out to OTLP endpoints based on their `Trace ID`

## Send traces

* Open third console window. Send [trace.json](./trace.json) payload to the `otelcol-agent` with help of a curl command:

  ```bash
  curl -X POST localhost:9411/api/v2/spans -H'Content-Type: application/json' -d @trace.json
  ```

  Notice there are two spans in the paylod which belong to two different traces.

* You should see in the `otelcol-agent` output that trace has been processed:

  ```text
  2022-05-29T12:56:04.420+0200	INFO	loggingexporter/logging_exporter.go:42	TracesExporter	{"#spans": 2}
  ```

* You should see in the `otlp-backend` console output one of the spans:

  ```text
  2022-05-29T12:56:04.421+0200	INFO	loggingexporter/logging_exporter.go:42	TracesExporter	{"#spans": 1}
  2022-05-29T12:56:04.421+0200	DEBUG	loggingexporter/logging_exporter.go:51	ResourceSpans #0
  Resource SchemaURL:
  Resource labels:
      -> service.name: STRING(one)
  ScopeSpans #0
  ScopeSpans SchemaURL:
  InstrumentationScope
  Span #0
      Trace ID       : 5982fe77008310cc80f1da5e10147519
      Parent ID      : 90394f6bcffb5d13
      ID             : 67fae42571535f68
      Name           : /m/n/2.6.1
      Kind           : SPAN_KIND_SERVER
      Start time     : 2018-01-24 08:16:15.726 +0000 UTC
      End time       : 2018-01-24 08:16:15.752 +0000 UTC
      Status code    : STATUS_CODE_UNSET
      Status message :
  Attributes:
      -> data.http_response_code: STRING(201)
      -> peer.service: STRING(one)
  ```

* You should be able to see second span in the newly created `data.json` file in the `otlp-backend` local file directory:

  ```json
  {"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"two"}}]},"scopeSpans":[{"scope":{},"spans":[{"traceId":"5982fe77008310cc80f1da5e10abf510","spanId":"67fae42571535f60","parentSpanId":"90394f6bcffb5d10","name":"/m/n/2.6.1","kind":"SPAN_KIND_SERVER","startTimeUnixNano":"1516781775726001000","endTimeUnixNano":"1516781775752001000","attributes":[{"key":"data.http_response_code","value":{"stringValue":"400"}},{"key":"peer.service","value":{"stringValue":"two"}}],"status":{}}]}]}]}
  ```

* Try changing the `traceId` to the same value in the [trace.json](./trace.json) file and sending data again. You should see data coming to the same OTLP endpoint (either `console output` or `data.json` file)
