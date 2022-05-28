# Environment variables in the OpenTelemetry Collector configuration

* Read the short excerpt from [Configuration Environment Variables documentation](https://opentelemetry.io/docs/collector/configuration/#configuration-environment-variables)

* Run the otelcol using prepared [config](config.yaml) file - it is a simple configuration with the static `service: my-static-name` added to all otelcol logs

  ```bash
  otelcol-contrib --config config.yaml
  ```

  You should notice that all the logs have the key-pair added, for example:

  ```text
  2022-05-28T10:48:53.393+0200	info	service/collector.go:146	Everything is ready. Begin running and processing data.	{"service": "my-static-name"}
  ```

* Change configuration to use the environment variable instead of a static value:

  ```yaml
  initial_fields:
    service: ${OT_SERVICE}
  ```

* Try running the otelcol without variable being set. As the variable is not set otelcol uses empty string now:

  ```text
  2022-05-28T10:51:35.107+0200	info	service/service.go:76	Starting extensions...	{"service": ""}
  ```

* Export the variable and run otelcol again. Notice that value from your environment variable is being used at this point:

  ```bash
  $ export OT_SERVICE="my-local-otc"
  $ otelcol-contrib --config config.yaml
  2022-05-28T10:54:05.093+0200	info	builder/exporters_builder.go:255	Exporter was built.	{"service": "my-local-otc", "kind": "exporter", "name": "logging"}
  2022-05-28T10:54:05.093+0200	info	builder/pipelines_builder.go:224	Pipeline was built.	{"service": "my-local-otc", "kind": "pipeline", "name": "logs"}
  ...
  ```
