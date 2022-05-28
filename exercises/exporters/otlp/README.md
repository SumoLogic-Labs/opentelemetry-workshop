# OTLP Exporter exercise

## Run the OTLP Backend

* For this exercise we need an OTLP listening backend. Let's use `otelcol` instance for that and reffer to it as `otlp-backend`

* Run the `otlp-backend` using the [config-otlp-backend.yaml](./config-otlp-backend.yaml) file, it will:
  * listen on `0.0.0.0:4317` address for insecure OTLP/gRPC connections with logs and traces
  * log all the incoming data to console using the `logging` exporter

  ```bash
  $ otelcol-contrib --config config-otlp-backend.yaml
  
  ...
  2022-05-28T21:35:27.719+0200	info	builder/receivers_builder.go:68	Receiver is starting...	{"kind": "receiver", "name": "otlp"}
  2022-05-28T21:35:27.719+0200	info	otlpreceiver/otlp.go:70	Starting GRPC server on endpoint 0.0.0.0:4317	{"kind": "receiver", "name": "otlp"}
  
  ...
  2022-05-28T21:35:27.719+0200	info	service/collector.go:146	Everything is ready. Begin running and processing data.
  ```

## Set exporting data from Otelcol Agent to the OTLP Backend

* Read the [OTLP Exporter documentation](https://github.com/open-telemetry/opentelemetry-collector/tree/v0.51.0/exporter/otlpexporter)

* Add the `OTLP exporter` to the [config.yaml](./config.yaml) file
  * remember to use insecure connection
  * keep the `logging` exporter, it will help debug problems

* In another console window, run the otelcol using updated [config](config.yaml) file - let's reffer to that instance as `otelcol-agent`:

  ```bash
  $ otelcol-contrib --config config.yaml
  
  ...
  2022-05-28T21:44:11.167+0200	info	service/service.go:81	Starting exporters...
  2022-05-28T21:44:11.167+0200	info	builder/exporters_builder.go:40	Exporter is starting...	{"kind": "exporter", "name": "otlp"}
  2022-05-28T21:44:11.167+0200	info	builder/exporters_builder.go:48	Exporter started.	{"kind": "exporter", "name": "otlp"}
  
  ...
  2022-05-28T21:44:11.168+0200	info	service/collector.go:146	Everything is ready. Begin running and processing data.
  ```

  This instance is listening on `localhost:12345` for TCP connections with logs and on `localhost:9411` for Zipkin traces

## Send logs

* Open third console window. Using the telnet command connect to `localhost:12345` and send some logs, eg. `Hey there, I'm log coming over TCP!`:

  ```bash
  $ telnet localhost 12345
  Trying ::1...
  Connected to localhost.
  Escape character is '^]'.
  Hey there, I'm log coming over TCP!
  ```

* You should see in the `otelcol-agent` output that log has been processed:

  ```text
  2022-05-28T21:55:42.409+0200	INFO	loggingexporter/logging_exporter.go:71	LogsExporter	{"#logs": 1}
  ```

* You should see in the `otlp-backend` output your log line:

  ```text
  2022-05-28T21:55:42.411+0200	INFO	loggingexporter/logging_exporter.go:71	LogsExporter	{"#logs": 1}
  2022-05-28T21:55:42.411+0200	DEBUG	loggingexporter/logging_exporter.go:81	ResourceLog #0
  Resource SchemaURL:
  ScopeLogs #0
  ScopeLogs SchemaURL:
  InstrumentationScope
  LogRecord #0
  ObservedTimestamp: 2022-05-28 19:55:42.320301 +0000 UTC
  Timestamp: 1970-01-01 00:00:00 +0000 UTC
  Severity:
  Body: Hey there, I'm log coming over TCP!
  Trace ID:
  Span ID:
  Flags: 0
  ```

* Close the telnet connection

## Send traces

* Send [trace.json](./trace.json) payload to the `otelcol-agent` with help of a curl command:

  ```bash
  curl -X POST localhost:9411/api/v2/spans -H'Content-Type: application/json' -d @trace.json
  ```

* You should see in the `otelcol-agent` output that trace has been processed:

  ```text
  2022-05-28T22:08:25.996+0200	INFO	loggingexporter/logging_exporter.go:42	TracesExporter	{"#spans": 1}
  ```

* You should see in the `otlp-backend` output your log line:

  ```text
  2022-05-28T22:08:25.999+0200	INFO	loggingexporter/logging_exporter.go:42	TracesExporter	{"#spans": 1}
  2022-05-28T22:08:25.999+0200	DEBUG	loggingexporter/logging_exporter.go:51	ResourceSpans #0
  Resource SchemaURL:
  Resource labels:
       -> service.name: STRING(api)
  ScopeSpans #0
  ScopeSpans SchemaURL:
  InstrumentationScope
  Span #0
      Trace ID       : 5982fe77008310cc80f1da5e10147519
      Parent ID      : 90394f6bcffb5d13
      ID             : 67fae42571535f60
      Name           : /m/n/2.6.1
      Kind           : SPAN_KIND_SERVER
      Start time     : 2018-01-24 08:16:15.726 +0000 UTC
      End time       : 2018-01-24 08:16:15.752 +0000 UTC
      Status code    : STATUS_CODE_UNSET
      Status message :
  Attributes:
       -> data.http_response_code: STRING(201)
       -> peer.service: STRING(apip)
  ```
