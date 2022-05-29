# OTLP Receiver exercise

OTLP protocol is one of the most important parts of the OpenTelemetry project. While here we show how to use it for traces, it can be used for logs and metrics as well.

* Run the otelcol using prepared [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

  You should see the following otelcol log lines:

  ```text
  2022-05-27T21:05:55.399+0200	info	otlpreceiver/otlp.go:88	Starting HTTP server on endpoint 0.0.0.0:4318	{"kind": "receiver", "name": "otlp"}
  2022-05-27T21:05:55.400+0200	info	builder/receivers_builder.go:73	Receiver started.	{"kind": "receiver", "name": "otlp"}
  ```

  At this point otelcol is litening on `0.0.0.0:4318` address waiting for incoming spans - building blocks for traces

* Spans can be created using the OpenTelemetry libraries available for many programming languages. They can be sent over HTTP as simple JSON as well.

  Send [trace.json](./trace.json) payload to your locally running otelcol instance with help of a `curl` command:

  ```bash
  $ curl -v "http://localhost:4318/v1/traces"  -H 'Content-type: application/json' -d @trace.json
  *   Trying 127.0.0.1:4318...
  * Connected to localhost (127.0.0.1) port 4318 (#0)
  > POST /v1/traces HTTP/1.1
  > Host: localhost:4318
  > User-Agent: curl/7.79.1
  > Accept: */*
  > Content-type: application/json
  > Content-Length: 857
  >
  * Mark bundle as not supporting multiuse
  < HTTP/1.1 200 OK
  < Content-Type: application/json
  < Date: Sun, 29 May 2022 08:16:21 GMT
  < Content-Length: 2
  <
  * Connection #0 to host localhost left intact
  {}
  ```

* In the `otelcol` logs output you should see the same span received:

  ```text
  2022-05-27T21:17:25.777+0200	INFO	loggingexporter/logging_exporter.go:42	TracesExporter	{"#spans": 1}
  2022-05-27T21:17:25.777+0200	DEBUG	loggingexporter/logging_exporter.go:51	ResourceSpans #0
  Resource SchemaURL:
  Resource labels:
       -> service.name: STRING(Some Service)
  ScopeSpans #0
  ScopeSpans SchemaURL:
  InstrumentationScope
  Span #0
      Trace ID       : 0000000000000000ffffff1653679045
      Parent ID      :
      ID             : ffffff1653679045
      Name           : console-test
      Kind           : SPAN_KIND_SERVER
      Start time     : 2022-05-27 19:17:25 +0000 UTC
      End time       : 2022-05-27 19:17:25.01 +0000 UTC
      Status code    : STATUS_CODE_UNSET
      Status message :
  Attributes:
       -> http.status_code: STRING(500)
       -> test: STRING(aaaaa-bbb)
       -> net.host.ip: STRING(192.168.1.1)
       -> net.host.port: INT(3333)
       -> net.peer.ip: STRING(172.19.0.80)
       -> net.peer.port: INT(4444)
  ```

* Play a bit with the [trace.json](./trace.json) payload, for example:
  * add the `spans.motto` key with `"there is no trace"` value to resource attributes (labels)
  * add the `use.otlp.for` key with `"all three: logs, metrics and traces"` value to the record attributes
