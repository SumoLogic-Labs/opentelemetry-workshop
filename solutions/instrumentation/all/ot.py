import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc._metric_exporter import OTLPMetricExporter

from opentelemetry.sdk._logs import (
    LogEmitterProvider,
    LoggingHandler,
    set_log_emitter_provider,
)

from opentelemetry.sdk._logs.export import (
    BatchLogProcessor,
    ConsoleLogExporter,
)

from opentelemetry.sdk._metrics import MeterProvider
from opentelemetry.sdk._metrics.export import PeriodicExportingMetricReader
from opentelemetry._metrics import set_meter_provider


from opentelemetry.sdk.trace import (
    TracerProvider,
)
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

console_enabled = False


def setup_tracer_provider():
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    if console_enabled:
        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


def setup_metric_provider():
    exporter = OTLPMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=15000)
    provider = MeterProvider(metric_readers=[reader])
    set_meter_provider(provider)


def setup_log_provider():
    log_emitter_provider = LogEmitterProvider()
    set_log_emitter_provider(log_emitter_provider)

    log_emitter_provider.add_log_processor(BatchLogProcessor(OTLPLogExporter()))
    if console_enabled:
        log_emitter_provider.add_log_processor(BatchLogProcessor(ConsoleLogExporter()))

    log_emitter = log_emitter_provider.get_log_emitter(__name__, "0.1")
    handler = LoggingHandler(level=logging.WARN, log_emitter=log_emitter)

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().addHandler(handler)
