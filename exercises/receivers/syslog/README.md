# Syslog Receiver exercise

* Run the otelcol using prepared [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

* Using another console window try sending some text, eg. `"test message"` with help of `telnet` command

  ```bash
  $ telnet localhost 54526
  Trying ::1...
  Connected to localhost.
  Escape character is '^]'.
  test message
  ```

  You should see a parsing `error` - that's because the `test message` does not comply with the [RFC 5424](https://datatracker.ietf.org/doc/html/rfc5424) format

* Try sending the example logs from the [RFC 5424](https://datatracker.ietf.org/doc/html/rfc5424#section-6.5) - notice how `severity` and other log attributes are automatically parsed

  ```text
  <165>1 2003-10-11T22:14:15.003Z mymachine.example.com evntslog - ID47 [exampleSDID@32473 iut="3" eventSource="Application" eventID="1011"][examplePriority@32473 class="high"]
  ```

  ```text
  <34>1 2003-10-11T22:14:15.003Z mymachine.example.com su - ID47 - BOM'su root' failed for lonvick on /dev/pts/8
  ```

  ```text
  <165>1 2003-08-24T05:14:15.000003-07:00 192.0.2.1 myproc 8710 - - %% It's time to make the do-nuts.
  ```

* Observe your data in the OTC logging output - you should see similar log lines:

  ```text
  2022-05-29T16:54:45.913+0200	INFO	loggingexporter/logging_exporter.go:71	LogsExporter	{"#logs": 1}
  2022-05-29T16:54:45.914+0200	DEBUG	loggingexporter/logging_exporter.go:81	ResourceLog #0
  Resource SchemaURL:
  ScopeLogs #0
  ScopeLogs SchemaURL:
  InstrumentationScope
  LogRecord #0
  ObservedTimestamp: 2022-05-29 14:54:45.845019 +0000 UTC
  Timestamp: 2003-08-24 12:14:15.000003 +0000 UTC
  Severity: Info2
  Body: <165>1 2003-08-24T05:14:15.000003-07:00 192.0.2.1 myproc 8710 - - %% It's time to make the do-nuts.
  Attributes:
      -> facility: INT(20)
      -> proc_id: STRING(8710)
      -> message: STRING(%% It's time to make the do-nuts.)
      -> version: INT(1)
      -> hostname: STRING(192.0.2.1)
      -> priority: INT(165)
      -> appname: STRING(myproc)
  Trace ID:
  Span ID:
  Flags: 0
  ```

* Read the [Syslog Receiver documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/receiver/syslogreceiver)

* Change the configuration to use the `rfc3164` protocol. Change the `location` to `Europe/Warsaw`. Using `telnet` send the following log and observe how the timestamp is automaticaly converted to UTC:

  ```text
  <34>Oct 11 22:14:15 mymachine su: 'su root' failed for lonvick
  ```
