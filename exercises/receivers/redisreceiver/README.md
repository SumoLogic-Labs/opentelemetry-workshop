# Redis Receiver exercise

* Run the Redis instance as a Docker container exposing it at `127.0.0.1:16379`:

  ```bash
  docker run --rm --name redis -d -p 127.0.0.1:16379:6379 redis
  ```

* Connect to Redis using the `telnet` command. When connected, issue the `INFO` command:

  ```bash
  $ telnet localhost 16379
  Trying ::1...
  Connected to localhost.
  Escape character is '^]'.
  INFO
  ```

  You should see information about your Redis instance

  ```text
  $4713
  # Server
  redis_version:7.0.0
  redis_git_sha1:00000000
  redis_git_dirty:0
  redis_build_id:1fad57151235ad0c
  redis_mode:standalone
  os:Linux 5.4.0-110-generic x86_64
  arch_bits:64
  ...
  ```

  To exit issue the `QUIT` command.

  Notice that Redis's INFO is different from the OpenTelemetry or Prometheus one, it uses it's own schema. We need `otelcol` be able to work with this schema - so it needs to be translated during ingestion. That's the job for the `Redis Receiver`.

* Read the [Redis Receiver documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.51.0/receiver/redisreceiver)

* Take a look at the [config.yaml](config.yaml) configuration file and run `otelcol` with this config locally:

  ```bash
  otelcol-contrib --config config.yaml
  ```

* You should see an error because your Redis instance is not running on a default `6379` port:

  ```text
  2022-05-22T10:01:15.032+0200	error	scraperhelper/scrapercontroller.go:198	Error scraping metrics	{"kind": "receiver", "name": "redis", "error": "dial tcp [::1]:6379: connect: connection refused", "scraper": "redis"}
  go.opentelemetry.io/collector/receiver/scraperhelper.(*controller).scrapeMetricsAndReport
    go.opentelemetry.io/collector@v0.51.0/receiver/scraperhelper/scrapercontroller.go:198
  go.opentelemetry.io/collector/receiver/scraperhelper.(*controller).startScraping.func1
    go.opentelemetry.io/collector@v0.51.0/receiver/scraperhelper/scrapercontroller.go:173
  ```

  The error is caused by this configuration line: `endpoint: $REDIS_ENDPOINT`. If there is no such variable in our environment the receiver tries to connect using default values.

* Export the environment variable end try running `otelcol` again:

  ```bash
  $ export REDIS_ENDPOINT=127.0.0.1:16379
  $ otelcol-contrib --config config.yaml
  ```

* You should be able to see the metrics ingested into `otelcol` at this point. Notice how they don't have any information about the host attached. We will show you how to do it in the [Resource Detection Processor exercise](../../processors/resourcedetection/). But that's later - for now go to the next step.

* Remove the Redis container:

  ```bash
  docker rm -f redis
  ```
