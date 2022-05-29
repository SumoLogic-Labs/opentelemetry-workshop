# Simple Prometheus Receiver exercise

For this excercise we need an application which will create and expose metrics in the Prometheus format. We'll reuse the OpenTelemetry Collector for that purpose as it exposes telemetry data in the Prometheus format by default.

## Otelcol instance for metrics creation

* Run the otelcol which will create and expose metrics using the prepared [config-data-creator.yaml](./config-data-creator.yaml) file. Keep it running.

  ```bash
  otelcol-contrib --config config-metrics-creator.yaml
  ```

  Examin the STDOUT logs - you should find a line similar to this one:

  ```text
  2022-05-21T12:33:09.631+0200	info	service/telemetry.go:129	Serving Prometheus metrics	{"address": ":8888", "level": "basic", "service.instance.id": "1822f5ba-2907-4a07-b786-70f5161c0ed5", "service.version": "latest"}
  ```

* In another console or in the web browser examin if metrics are exposed under [http://localhost:8888/metrics](http://localhost:8888/metrics). You should see output similar to this one:

  ```bash
  $ curl localhost:8888/metrics
  # HELP otelcol_exporter_enqueue_failed_log_records Number of log records failed to be added to the sending queue.
  # TYPE otelcol_exporter_enqueue_failed_log_records counter
  otelcol_exporter_enqueue_failed_log_records{exporter="logging",service_instance_id="caaa9fe6-8dad-458d-a6bc-8d7e1f0fd4c2",service_version="latest"} 0
  # HELP otelcol_exporter_enqueue_failed_metric_points Number of metric points failed to be added to the sending queue.
  # TYPE otelcol_exporter_enqueue_failed_metric_points counter
  otelcol_exporter_enqueue_failed_metric_points{exporter="logging",service_instance_id="caaa9fe6-8dad-458d-a6bc-8d7e1f0fd4c2",service_version="latest"} 0
  # HELP otelcol_exporter_enqueue_failed_spans Number of spans failed to be added to the sending queue.
  # TYPE otelcol_exporter_enqueue_failed_spans counter
  otelcol_exporter_enqueue_failed_spans{exporter="logging",service_instance_id="caaa9fe6-8dad-458d-a6bc-8d7e1f0fd4c2",service_version="latest"} 0
  # HELP otelcol_process_cpu_seconds Total CPU user and system time in seconds
  # TYPE otelcol_process_cpu_seconds gauge
  otelcol_process_cpu_seconds{service_instance_id="caaa9fe6-8dad-458d-a6bc-8d7e1f0fd4c2",service_version="latest"} 1.9900000000000002
  # HELP otelcol_process_memory_rss Total physical memory (resident set size)
  # TYPE otelcol_process_memory_rss gauge
  otelcol_process_memory_rss{service_instance_id="caaa9fe6-8dad-458d-a6bc-8d7e1f0fd4c2",service_version="latest"} 4.6800896e+07
  # HELP otelcol_process_runtime_heap_alloc_bytes Bytes of allocated heap objects (see 'go doc runtime.MemStats.HeapAlloc')
  # TYPE otelcol_process_runtime_heap_alloc_bytes gauge
  otelcol_process_runtime_heap_alloc_bytes{service_instance_id="caaa9fe6-8dad-458d-a6bc-8d7e1f0fd4c2",service_version="latest"} 8.65612e+06
  # HELP otelcol_process_runtime_total_alloc_bytes Cumulative bytes allocated for heap objects (see 'go doc runtime.MemStats.TotalAlloc')
  # TYPE otelcol_process_runtime_total_alloc_bytes gauge
  otelcol_process_runtime_total_alloc_bytes{service_instance_id="caaa9fe6-8dad-458d-a6bc-8d7e1f0fd4c2",service_version="latest"} 2.3425576e+07
  # HELP otelcol_process_runtime_total_sys_memory_bytes Total bytes of memory obtained from the OS (see 'go doc runtime.MemStats.Sys')
  # TYPE otelcol_process_runtime_total_sys_memory_bytes gauge
  otelcol_process_runtime_total_sys_memory_bytes{service_instance_id="caaa9fe6-8dad-458d-a6bc-8d7e1f0fd4c2",service_version="latest"} 2.682164e+07
  # HELP otelcol_process_uptime Uptime of the process
  # TYPE otelcol_process_uptime counter
  otelcol_process_uptime{service_instance_id="caaa9fe6-8dad-458d-a6bc-8d7e1f0fd4c2",service_version="latest"} 1230.0165619999998
  ```

  Keep this otelcol instance running. We will need it for the rest of this exercise.

## Second otelcol instance for metrics collection

At this point we need a second otelcol instance which will scrape Prometheus metrics from the first instance.

* Read the [Simple Prometheus Receiver documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/receiver/simpleprometheusreceiver)

* Change [config.yaml](./config.yaml) configuration file for the second otelcol instance by adding the `.receivers.prometheus_simple.endpoint` key. The endpoint shold be pointing to metrics endpoint of the first otelcol instance.

* In another console run the second otelcol instance

  ```bash
  otelcol-contrib --config config.yaml
  ```

  Now you should see a similar error:

  ```text
  2022-05-21T12:51:21.550+0200	error	service/collector.go:174	Asynchronous error received, terminating process	{"error": "listen tcp :8888: bind: address already in use"}
  ```

  That's because it tries to serve metrics at [http://localhost:8888](http://localhost:8888) - but our first process is already using that address!  
  Change [config.yaml](./config.yaml) configuration file for the second otelcol instance by changing the `.service.telemetry.metrics.address` key. Try using the `0.0.0.0:8889` address and running otelcol again.

## Question

How many metrics you get vs how many are exposed at [http://localhost:8888/metrics](http://localhost:8888/metrics)? Can you find what are the additional ones? Try changing the `.exporters.logging.loglevel=debug` to find out.

## Autoscrape

* Try adding configuration to scrape second otelcol own metrics. They should be available at `0.0.0.0:8889` address. Can you differentiate between metrics from first and second otelcol instances?

  Hint: check the `resource attributes` and `record attributes`
