# Tail Sampling Processor exercise

* Take a look at the [config.yaml](config.yaml) configuration file and run `otelcol` with this config locally

  ```bash
  otelcol-contrib --config config.yaml
  ```

  It is listening for spans using the OTLP Receiver

* In your console, send a trace using the [send-trace.sh](./send-trace.sh) script. It is a simple wrapper over `curl` command with a trace payload

  ```bash
  $ ./send-trace.sh
  + curl -v http://localhost:4318/v1/traces -H 'Content-type: application/json' --data-raw '{"resourceSpans":[{
  ...
  ```

  You should be able to observe 2 spans coming in the `otelcol` output:

  ```text
  2022-05-29T11:54:59.130+0200	INFO	loggingexporter/logging_exporter.go:42	TracesExporter	{"#spans": 2}
  2022-05-29T11:54:59.130+0200	DEBUG	loggingexporter/logging_exporter.go:51	ResourceSpans #0
  Resource SchemaURL:
  Resource labels:
      -> service.name: STRING(Some Service)
  ScopeSpans #0
  ScopeSpans SchemaURL:
  InstrumentationScope
  Span #0
      Trace ID       : 0000000000000000ffffff1653818099
      Parent ID      :
      ID             : ffffff1653818099
      Name           : some-service-span
      Kind           : SPAN_KIND_SERVER
      Start time     : 2022-05-29 09:54:59 +0000 UTC
      End time       : 2022-05-29 09:54:59.01 +0000 UTC
      Status code    : STATUS_CODE_OK
      Status message :
  Attributes:
      -> net.peer.port: INT(4444)
  Span #1
      Trace ID       : 0000000000000000ffffff1653818099
      Parent ID      :
      ID             : fffffa1653818099
      Name           : some-service-span
      Kind           : SPAN_KIND_SERVER
      Start time     : 2022-05-29 09:54:59.02 +0000 UTC
      End time       : 2022-05-29 09:54:59.03 +0000 UTC
      Status code    : STATUS_CODE_OK
      Status message :
  Attributes:
      -> net.peer.port: INT(4444)
  ```

  Notice that both spans status code is `OK`.

* Read the [Tail Sampling Processor documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/processor/tailsamplingprocessor)

* We would like to filter out all the traces with status `OK` or `UNSET` and catch only those ones which resulted with an `ERROR`. Using the Tail Sampling Processor add the following config:

  ```text
  decision_wait: 1s
  num_traces: 1
  expected_new_traces_per_sec: 1
  policies:
    [
        {
          name: catch_errors,
          type: status_code,
          status_code: {status_codes: [ERROR]}
        }
    ]
  ```

* In your console, try sending trace using the [send-trace.sh](./send-trace.sh) script again. You should observe that your traces are filter out now in the `otelcol` output

  ```bash
  $ ./send-trace.sh
  + curl -v http://localhost:4318/v1/traces -H 'Content-type: application/json' --data-raw '{"resourceSpans":[{
  ...
  ```

* Update the [send-trace.sh](./send-trace.sh) script by changing status code for one or both of the spans to `ERROR`:

  ```json
  "code":"STATUS_CODE_OK"
  ```

* Send trace with updategd [send-trace.sh](./send-trace.sh) script again. Now you should see trace in the `otelcol` output
