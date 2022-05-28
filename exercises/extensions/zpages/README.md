# zPages Extension exercise

* Read the [zPages Extension documentation](https://github.com/open-telemetry/opentelemetry-collector/blob/v0.51.0/extension/zpagesextension/README.md)

* Run the otelcol instance using the prepared [config](config.yaml) file - it is a simple configuration without any extensions added

  ```bash
  otelcol-contrib --config config.yaml
  ```

* Add the zPages extension to you otelcol configuration by adding the following keys:

  ```yaml
  extensions:
    zpages:

  service:
    extensions: [zpages]
  ```

* Run otelcol again, you should be able to see that zPages has been enabled:

  ```text
  2022-05-28T18:43:00.005+0200	info	zpagesextension/zpagesextension.go:40	Register Host's zPages	{"kind": "extension", "name": "zpages"}
  2022-05-28T18:43:00.007+0200	info	zpagesextension/zpagesextension.go:53	Starting zPages extension	{"kind": "extension", "name": "zpages", "config": {"TCPAddr":{"Endpoint":"localhost:55679"}}}
  ```

* While still running otelcol, check with web browser one of the default zPages routes, for example [http://localhost:55679/debug/servicez](http://localhost:55679/debug/servicez) - you should be able to see the overview of the collector services

* Check the other exposed zPages routes - list can be found in the [zPages Extension documentation](https://github.com/open-telemetry/opentelemetry-collector/blob/v0.51.0/extension/zpagesextension/README.md) mentioned above
