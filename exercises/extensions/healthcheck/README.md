# Health Check Extension exercise

* Read the [Health Check Extension documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/v0.51.0/extension/healthcheckextension/README.md)

* Run the otelcol using prepared [config](config.yaml) file - it is a simple configuration without any extensions added

  ```bash
  otelcol-contrib --config config.yaml
  ```

* Add the Health Check extension to you otelcol configuration by adding the following keys:

  ```yaml
  extensions:
    health_check:

  service:
    extensions: [health_check]
  ```

* Run otelcol again, you should be able to see that Health Check has been enabled:

  ```text
  2022-05-28T08:48:56.999+0200	info	extensions/extensions.go:38	Extension is starting...	{"kind": "extension", "name": "health_check"}
  2022-05-28T08:48:56.999+0200	info	healthcheckextension@v0.51.0/healthcheckextension.go:44	Starting health_check extension	{"kind": "extension", "name": "health_check", "config": {"Port":0,"TCPAddr":{"Endpoint":"0.0.0.0:13133"},"Path":"/","CheckCollectorPipeline":{"Enabled":false,"Interval":"5m","ExporterFailureThreshold":5}}}
  ```

* While still running otelcol, check the health status that is exposed at the default [http://localhost:13133](http://localhost:13133). You can do that using the web browser or with help of `curl` and `jq` commands run in other console window:

  ```bash
  $ curl -s localhost:13133 | jq
  {
    "status": "Server available",
    "upSince": "2022-05-28T08:48:57.003639+02:00",
    "uptime": "8m19.627506344s"
  }
  ```
