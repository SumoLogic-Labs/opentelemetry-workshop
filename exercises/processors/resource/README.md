# Resource Processor exercise

Whenever you need to modify attributes of a log, metric or span at the resource level you can use the Resource Processor.

* Run the otelcol using prepared [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

  Notice that Resource Detection processor has been used, and two resource labels has been added:

  ```text
  Resource labels:
     -> host.name: STRING(lolcathost)
     -> os.type: STRING(linux)
  ```

* Read the [Resource Processor documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/processor/resourceprocessor)

* Using the Resource Processor insert `my.custom.attribute` attribute with `my custom value` value

* Try renaming the `host.name` attribute to just `host`. You may need to create new attribute and delete the old one.
