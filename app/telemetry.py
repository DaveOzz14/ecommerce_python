"""OpenTelemetry configuration module for traces, metrics, and logs."""
import os
import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.logging import LoggingInstrumentor


def configure_telemetry():
    """Configure OpenTelemetry providers for traces, metrics, and logs."""
    
    # Resource configuration from environment
    resource = Resource.create(
        {
            "service.name": os.getenv("OTEL_SERVICE_NAME", "ecommerce-python"),
            "service.version": "1.0.0",
            "deployment.environment": os.getenv("OTEL_RESOURCE_ATTRIBUTES", "deployment.environment=production").split("=")[1]
        }
    )
    
    # Configure Tracer Provider
    trace_provider = TracerProvider(resource=resource)
    otlp_trace_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"),
        headers={"Authorization": os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "").replace("Authorization=", "")}
    )
    trace_provider.add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
    trace.set_tracer_provider(trace_provider)
    
    # Configure Meter Provider
    otlp_metric_exporter = OTLPMetricExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_METRICS_ENDPOINT"),
        headers={"Authorization": os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "").replace("Authorization=", "")}
    )
    metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter, export_interval_millis=60000)
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    
    # Configure Logger Provider
    logger_provider = LoggerProvider(resource=resource)
    otlp_log_exporter = OTLPLogExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT"),
        headers={"Authorization": os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "").replace("Authorization=", "")}
    )
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))
    
    # Attach OTEL handler to root logger
    handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    
    # Instrument logging for trace correlation
    LoggingInstrumentor().instrument(set_logging_format=True)
    
    return trace_provider, meter_provider, logger_provider


def get_tracer(name: str):
    """Get a tracer instance."""
    return trace.get_tracer(name)


def get_meter(name: str):
    """Get a meter instance."""
    return metrics.get_meter(name)
