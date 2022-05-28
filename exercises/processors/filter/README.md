# Filter Processor exercise

Whenever you need to filter out logs or metrics you can use the Filter Processor.

* Read the [Filter Processor documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/processor/filterprocessor)

## Logs

* Run the otelcol using prepared [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

  You should see three logs collected: two from `lolcathost` and one from `foobarhost`

* Add filter processor to the logs pipeline. Configure it to exclude those logs coming from `foo.*` hosts using the `host` record attribute

  You should see only two logs comming from the `lolcathost` at this point

## Metrics

* Uncomment `hostmetrics receiver` and `metrics pipeline` sections in the [config](config.yaml) file. Run otelcol.

  In addition to logs you should also see some load metrics coming in, such as:

  ```text
  system.cpu.load_average.1m
  system.cpu.load_average.5m
  system.cpu.load_average.15m
  ```

* Use the filter processor to exclude all the metrics which name match following regex: `system.cpu.load_average.1.*`

  You should get the `system.cpu.load_average.5m` metric only at this point
