import logging

from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

from opentelemetry.sdk._logs import (
    LogEmitterProvider,
    LoggingHandler,
    set_log_emitter_provider,
)

from opentelemetry.sdk._logs.export import (
    BatchLogProcessor,
    ConsoleLogExporter,
)


console_enabled = False


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
