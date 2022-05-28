# File Exporter exercise

* Run the otelcol instance using the prepared [config](config.yaml) file

  ```bash
  otelcol-contrib --config config.yaml
  ```

  You should see the details of two log lines from [logs.txt](./logs.txt) file that were ingested and processed:

  ```text
  ...
  2022-05-28T20:31:58.847+0200	INFO	loggingexporter/logging_exporter.go:71	LogsExporter	{"#logs": 2}
  2022-05-28T20:31:58.850+0200	DEBUG	loggingexporter/logging_exporter.go:81	ResourceLog #0
  Resource SchemaURL:
  ...
  ```

* Read the [File Exporter documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/exporter/fileexporter)

* Change the configuration to export those logs into a JSON file `logs.json` in a local directory and run otelcol again

  You should now see that new `logs.json` file has been created

* Take a look at the JSON structure in `logs.json` file - the `jq` command might be helpful here:

  ```bash
  $ cat logs.json | jq
  {
    "resourceLogs": [
      {
        "resource": {},
        "scopeLogs": [
          {
            "scope": {},
            "logRecords": [
  ...
  ```

  You should be able to find `host`, `type` and `foo` attributes in there

* Run otelcol once again, the `logs.txt` file will be collected from beginning. What happened to the `logs.json` file? How to prevent that?
