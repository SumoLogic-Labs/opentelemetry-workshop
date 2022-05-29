# Service Telemetry in the OpenTelemetry Collector configuration

* Read the short excerpt on [Service Telemetry documentation](https://opentelemetry.io/docs/collector/configuration/#service)

## Metrics

* Run the otelcol using prepared [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

  You should see a similar log line in your otelcol logs:

  ```text
  2022-05-28T11:52:29.226+0200	info	service/telemetry.go:129	Serving Prometheus metrics	{"address": ":8888", "level": "basic", "service.instance.id": "0490fae5-3ac4-445e-bf5d-ef6c78a9bee9", "service.version": "latest"}
  ```

* While still running otelcol, check the telemetry data that is exposed at the default endpoint [http://localhost:8888/metrics](http://localhost:8888/metrics). You can do that using the web browser or with help of `curl` command run in other console window:

  ```bash
  $ curl -s localhost:8888/metrics
  # HELP otelcol_exporter_enqueue_failed_log_records Number of log records failed to be added to the sending queue.
  # TYPE otelcol_exporter_enqueue_failed_log_records counter
  otelcol_exporter_enqueue_failed_log_records{exporter="logging",service_instance_id="0490fae5-3ac4-445e-bf5d-ef6c78a9bee9",service_version="latest"} 0
  # HELP otelcol_exporter_enqueue_failed_metric_points Number of metric points failed to be added to the sending queue.
  # TYPE otelcol_exporter_enqueue_failed_metric_points counter
  otelcol_exporter_enqueue_failed_metric_points{exporter="logging",service_instance_id="0490fae5-3ac4-445e-bf5d-ef6c78a9bee9",service_version="latest"} 0
  ...
  ```

* Try changing the port on which metrics are exposed, eg. to `address: 0.0.0.0:18888`; confirm metrics are exposed there

* You can also disable the telemetry metrics altogether. Try that with the help of `level: none` configuration option. You should see the following log line:

  ```text
  2022-05-28T12:00:52.882+0200	info	service/telemetry.go:101	Skipping telemetry setup.	{"address": "0.0.0.0:18888", "level": "none"}
  ```

  Also you can confirm metrics are not exposed anymore with `curl` or in the browser at [https://localhost:18888](https://localhost:18888)

  ```bash
  $ curl localhost:18888/metrics
  curl: (7) Failed to connect to localhost port 18888 after 9 ms: Connection refused
  ```

## Logs

* By default otelcol has log level set to `info`. Try changing it to `warn` - unless there are any warnings or errors you should not see any logs at all. You could confirm it is working but you would need telemetry metrics enabled for that.

* Change the log level back to `info`

* Now let's try adding some metadata to every log line produced by otelcol with the help of `initial_fields`. Add the `service: my-otc-instance` to logs

* Run otelcol. You should see metatada added to every log line, for example:

  ```text
  2022-05-28T12:31:36.261+0200	info	service/collector.go:146	Everything is ready. Begin running and processing data.	{"service": "my-otc-instance"}
  ```
