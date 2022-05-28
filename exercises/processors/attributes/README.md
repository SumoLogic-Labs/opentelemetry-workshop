# Attributes Processor exercise

Whenever you need to modify attributes of a log, metric or span at the record level you can use the Attributes Processor.

* Run the otelcol using prepared [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

* Read the [Attributes Processor documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/processor/attributesprocessor)

* Using the Attributes Processor insert `my.custom.attribute` attribute with `my custom value` value. You should see this attribute added to every record:

  ```text
  Data point attributes:
     -> my.custom.attribute: STRING(my custom value)
  ```
