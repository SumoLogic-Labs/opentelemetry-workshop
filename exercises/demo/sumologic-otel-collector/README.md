# Sumo Logic OpenTelemetry Collector exercise

## Download Sumo Logic OpenTelemetry Collector

* For this exercise we need a [Sumo Logic distribution of OpenTelemetry Collector](https://github.com/SumoLogic/sumologic-otel-collector) - we'll reffer to is as `otelcol-sumo`

* Download `otelcol-sumo` binary from [the releases page](https://github.com/SumoLogic/sumologic-otel-collector/releases/tag/v0.51.0-sumo-0), rename is as `otelcol-sumo` and add it to your `PATH` environment variable

  For example here are commands you can run on `Linux` machine using the `amd64` processor:

  ```bash
  mkdir ~/otelcol-sumo

  cd ~/otelcol-sumo
  
  wget https://github.com/SumoLogic/sumologic-otel-collector/releases/download/v0.51.0-sumo-0/otelcol-sumo-0.51.0-sumo-0-linux_amd64
  
  mv otelcol-sumo-0.51.0-sumo-0-linux_amd64 otelcol-sumo
  
  chmod +x otelcol-sumo
  
  export PATH="$PATH":~/otelcol-sumo
  ```

* Set the `SUMOLOGIC_TOKEN` environment variable - you should already have a token from the [prerequisites](../prerequisites) step

  ```bash
  export SUMOLOGIC_TOKEN=your-sumologic-token
  ```

* Run the `otelcol-sumo` using prepared [config](config.yaml) file

  ```bash
  otelcol-sumo --config config.yaml
  ```

  By default it creates a collector in the Sumo Backend and forwards there content of the [logs.txt](./logs.txt) file - you should see is in the `otelcol-sumo` output:

  ```text
  2022-05-29T18:27:18.673+0200	info	builder/exporters_builder.go:48	Exporter started.	{"kind": "exporter", "name": "sumologic"}
  ...

  2022-05-29T18:27:18.878+0200	info	file/file.go:174	Started watching file	{"kind": "receiver", "name": "filelog", "operator_id": "file_input", "operator_type": "file_input", "path": "logs.txt"}
  2022-05-29T18:27:19.208+0200	INFO	loggingexporter/logging_exporter.go:71	LogsExporter	{"#logs": 3}
  ```

* Go to [Sumo Logic > New > Log Search](https://help.sumologic.com/05Search/Get-Started-with-Search/Search-Basics/About-Search-Basics) and see if your logs are visible; you might need to wait a couple of seconds for them to appear
