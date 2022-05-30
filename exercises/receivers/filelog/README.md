# Filelog Receiver exercise

* Run the otelcol using prepared [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

  You should see that it is ready to run and process data:

  ```text
  2022-05-27T14:58:22.340+0200	info	service/collector.go:146	Everything is ready. Begin running and processing data.
  2022-05-27T14:58:22.541+0200	info	file/file.go:176	Started watching file from end. To read preexisting logs, configure the argument 'start_at' to 'beginning'	{"kind": "receiver", "name": "filelog", "operator_id": "file_input", "operator_type": "file_input", "path": "logs.txt"}
  ```

* Consult provided [logs.txt](./logs.txt) file. Log lines are there but were not collected

## Simple configuration

* Read the [Filelog Receiver documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/receiver/filelogreceiver)

* Change configuration to read from the beginning of the file using `start_at: beginning`

  You should now see that `otelcol` received 2 log lines:

  ```text
  2022-05-27T15:02:00.946+0200	INFO	loggingexporter/logging_exporter.go:71	LogsExporter	{"#logs": 2}
  ```

* Change the Logging Exporter configuration section to show all the log details by using `loglevel: debug` option

  Now you should be able to see much more details:

  ```text
  LogRecord #0
  ObservedTimestamp: 2022-05-27 13:05:06.733652 +0000 UTC
  Timestamp: 1970-01-01 00:00:00 +0000 UTC
  Severity:
  Body: WARN Host=lolcathost, Type=laptop Hello World, high severity
  Attributes:
       -> log.file.name: STRING(logs.txt)
  Trace ID:
  Span ID:
  Flags: 0
  ```

* Change the configuration to:
  * remove file name using `include_file_name: false`
  * include the resolved file path using `include_file_path_resolved: true`

  You should see the full path to file now:

  ```text
  Body: WARN Host=lolcathost, Type=laptop Hello World, high severity
  Attributes:
       -> log.file.path_resolved: STRING(/my/path/to/opentelemetry-workshop/exercises/receivers/filelog/logs.txt)
  ```

* Change configuration to include the following record attribute: `foo: bar`

  You should be able to see this attribute in otelcol's output:

  ```text
  Body: DEBUG Host=lolcathost, Type=laptop Hello World, low severity
  Attributes:
       -> foo: STRING(bar)
       -> log.file.path_resolved: STRING(/my/path/to/opentelemetry-workshop/exercises/receivers/filelog/logs.txt)
  ```

## Regex Parser Operator

* Take a look at the [Regex Parser Operator documentation](https://github.com/open-telemetry/opentelemetry-log-collection/blob/v0.29.1/docs/operators/regex_parser.md#example-configurations)

* Using the following regex parser operator definition add `Host` and `Type` to record attributes

  ```text
  parsers:
    - id: regex-parse
      type: regex_parser
      parse_from: body
      regex: 'Host=(?P<host>[^,]+), Type=(?P<type>[^\s]+)'
  ```

  Run otelcol again. You should see similar output:

  ```text
  Body: WARN Host=lolcathost, Type=laptop Hello World, high severity
  Attributes:
       -> log.file.path_resolved: STRING(/my/path/to/opentelemetry-workshop/exercises/receivers/filelog/logs.txt)
       -> foo: STRING(bar)
       -> host: STRING(lolcathost)
       -> type: STRING(laptop)
  ```

  Having those attributes now you could for example filter out some of the logs. We'll show you later how to do that in the [Filter Processor](../../processors/filter/) exercise.

* Take a look at this [available operators list](https://github.com/open-telemetry/opentelemetry-log-collection/tree/v0.29.1/docs/operators#what-operators-are-available). They allow for many useful actions while collecting logs. Their functionaly also overlaps with some of the processors sometimes.
