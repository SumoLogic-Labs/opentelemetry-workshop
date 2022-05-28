# Instrumenting simple Python app

In this set we will work with a trivial Python service - `server`, which is built on top of Flask
and has a sole purpose of calculating a Fibonacci number.

There's also another process we will use - a `client`, which iterates over a set of numbers and calls
the server.

[Python instrumentation guide available at OpenTelemetry.io website](https://opentelemetry.io/docs/instrumentation/python/getting-started/).

[Intro to OpenTelemetry data model concepts](slides) (can be run via [markdeck](https://github.com/arnehilmann/markdeck))

1. [Warmup](plain)
2. [Logs](logs)
3. [Metrics](metrics)
4. [Traces](traces)
