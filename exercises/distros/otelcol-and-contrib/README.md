# Steps to follow

* Download the `OpenTelemetry Collector Contrib` - also called `otelcol-contrib` version `v0.51.0` from the [contrib releases page](https://github.com/open-telemetry/opentelemetry-collector-contrib/releases/tag/v0.51.0)

* Unpack or install it in the system. Add to your shell's `PATH` variable for easier usage.

* Find out which otelcol version you use. This workshop has been prepared using `v0.51.0`

  ```bash
  otelcol-contrib --version
  ```

* Make sure to use proper documentation version on GitHub using the git branch, eg. `release/v0.51.x`

* Run the otelcol using prepared [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

* Check if otelcol is available on `localhost:4318`

  ```bash
  telnet localhost 4318
  ```

* Check if otelcol exposes Prometheus metrics

  ```bash
  curl localhost:8888/metrics
  ```

* Check out the Core Distro components:
  * receivers: https://github.com/open-telemetry/opentelemetry-collector/tree/main/receiver
  * processors: https://github.com/open-telemetry/opentelemetry-collector/tree/main/processor
  * exporter: https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter

* Check out what is actually built into distributions:
  * otelcol: https://github.com/open-telemetry/opentelemetry-collector-releases/blob/main/distributions/otelcol/manifest.yaml
  * otelcol-contrib: https://github.com/open-telemetry/opentelemetry-collector-releases/blob/main/distributions/otelcol-contrib/manifest.yaml

* You can check that `kafkareceiver` is included in core distro
