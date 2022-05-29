# Zipkin Receiver exercise

* Read the [Zipkin Receiver documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/receiver/zipkinreceiver)

* Update the [config](config.yaml) file by adding Zipkin receiver with default values

* Run the otelcol using your updated [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

  You should see the following otelcol logs in the output:

  ```text
  2022-05-29T16:33:55.267+0200	info	service/service.go:91	Starting receivers...
  2022-05-29T16:33:55.267+0200	info	builder/receivers_builder.go:68	Receiver is starting...	{"kind": "receiver", "name": "zipkin"}
  2022-05-29T16:33:55.268+0200	info	builder/receivers_builder.go:73	Receiver started.	{"kind": "receiver", "name": "zipkin"}
  ```

  At this point otelcol is litening on `0.0.0.0:9411` address waiting for incoming spans in Zipkin format

* Send [trace.json](./trace.json) payload to your locally running otelcol instance with help of a `curl` command:

  ```bash
  $ curl -v localhost:9411/api/v2/spans -H'Content-Type: application/json' -d @trace.json
  *   Trying 127.0.0.1:9411...
  * Connected to localhost (127.0.0.1) port 9411 (#0)
  > POST /api/v2/spans HTTP/1.1
  > Host: localhost:9411
  > User-Agent: curl/7.79.1
  > Accept: */*
  > Content-Type: application/json
  > Content-Length: 390
  >
  * Mark bundle as not supporting multiuse
  < HTTP/1.1 202 Accepted
  < Date: Sun, 29 May 2022 14:38:37 GMT
  < Content-Length: 0
  <
  * Connection #0 to host localhost left intact
  ```

* In the `otelcol` logs output you should see the same span received:

  ```text
  2022-05-29T16:38:37.097+0200	INFO	loggingexporter/logging_exporter.go:42	TracesExporter	{"#spans": 1}
  2022-05-29T16:38:37.097+0200	DEBUG	loggingexporter/logging_exporter.go:51	ResourceSpans #0
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

* Take a look at the [Jaeger receiver documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/receiver/jaegerreceiver) - otelcol can read spans in `Jaeger` format as well
