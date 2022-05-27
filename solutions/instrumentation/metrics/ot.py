from opentelemetry.exporter.otlp.proto.grpc._metric_exporter import OTLPMetricExporter

from opentelemetry.sdk._metrics import MeterProvider
from opentelemetry.sdk._metrics.export import PeriodicExportingMetricReader
from opentelemetry._metrics import set_meter_provider


def setup_metric_provider():
    exporter = OTLPMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=15000)
    provider = MeterProvider(metric_readers=[reader])
    set_meter_provider(provider)

