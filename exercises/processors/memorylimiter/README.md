# Memory Limiter exercise

It is recommended to limit the otelcol's memory usage early in the processors pipeline.

* Run the otelcol using prepared [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

  You should see logs and metrics coming in:

  ```text
  2022-05-24T14:57:42.568+0200	INFO	loggingexporter/logging_exporter.go:71	LogsExporter	{"#logs": 12}
  2022-05-24T14:57:47.267+0200	INFO	loggingexporter/logging_exporter.go:56	MetricsExporter	{"#metrics": 3}
  2022-05-24T14:57:52.267+0200	INFO	loggingexporter/logging_exporter.go:56	MetricsExporter	{"#metrics": 3}
  ```

* Read the [Memory Limiter documentation](https://github.com/open-telemetry/opentelemetry-collector/blob/v0.51.0/processor/memorylimiterprocessor/README.md)

* Limit maximum memory usage for to the `logs pipeline` to 4mb

  You should see that metrics are comming in while logs are not:

  ```text
  2022-05-24T14:51:23.332+0200	info	memorylimiterprocessor/memorylimiter.go:271	Memory usage after GC.	{"kind": "processor", "name": "memory_limiter/logs", "pipeline": "logs", "cur_mem_mib": 9}
  2022-05-24T14:51:24.329+0200	warn	memorylimiterprocessor/memorylimiter.go:281	Memory usage is above hard limit. Forcing a GC.	{"kind": "processor", "name": "memory_limiter/logs", "pipeline": "logs", "cur_mem_mib": 9}
  2022-05-24T14:51:24.330+0200	INFO	loggingexporter/logging_exporter.go:56	MetricsExporter	{"#metrics": 3}
  ```

* Change the logs pipeline memory limit to 128mb. You should see that the `logs pipeline` is working fine.

* Limit maximum memory usage for the `metrics pipeline` to 4mb. Do not change the memory limit for the `logs pipeline`.

  `Metrics pipeline` should not work at this point and you should see warning in otelcol logs. You should not see error from the `logs pipeline`:

  ```text
  2022-05-24T14:54:53.071+0200	INFO	loggingexporter/logging_exporter.go:71	LogsExporter	{"#logs": 12}
  2022-05-24T14:54:53.770+0200	warn	memorylimiterprocessor/memorylimiter.go:281	Memory usage is above hard limit. Forcing a GC.	{"kind": "processor", "name": "memory_limiter/metrics", "pipeline": "metrics", "cur_mem_mib": 10}
  2022-05-24T14:54:53.773+0200	info	memorylimiterprocessor/memorylimiter.go:271	Memory usage after GC.	{"kind": "processor", "name": "memory_limiter/metrics", "pipeline": "metrics", "cur_mem_mib": 9}
  ```

* Change the `metrics pipeline` memory limit to 64mb. You should have both logs and metrics pipelines working OK again.

  ```text
  2022-05-24T15:01:40.306+0200	INFO	loggingexporter/logging_exporter.go:71	LogsExporter	{"#logs": 12}
  2022-05-24T15:01:45.006+0200	INFO	loggingexporter/logging_exporter.go:56	MetricsExporter	{"#metrics": 3}
  2022-05-24T15:01:50.005+0200	INFO	loggingexporter/logging_exporter.go:56	MetricsExporter	{"#metrics": 3}
  ```
