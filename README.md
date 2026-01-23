# E-commerce Python Application with OpenTelemetry

Production-ready FastAPI e-commerce application instrumented with OpenTelemetry for comprehensive observability.

## Features

- **FastAPI Backend** - Modern async web framework
- **Jinja2 Templates** - Server-side rendering
- **Full OpenTelemetry Integration**:
  - ✅ Distributed Tracing
  - ✅ Metrics (RED + Custom)
  - ✅ Structured Logs with Trace Correlation
  - ✅ Automatic HTTP instrumentation
  - ✅ Manual business spans

## Architecture

```
ecommerce_python/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with OTEL bootstrap
│   ├── telemetry.py         # OpenTelemetry configuration
│   ├── routers/
│   │   ├── auth.py          # Login with manual spans
│   │   ├── products.py      # Product catalog with tracing
│   │   └── checkout.py      # Checkout flow with tracing
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS assets
├── requirements.txt         # Python dependencies
├── .env                     # OTLP configuration (DO NOT COMMIT)
└── .env.example             # Template for environment vars
```

## OpenTelemetry Configuration

All OTLP settings are configured via environment variables in `.env`:

- **Service Name**: `ecommerce-python`
- **Protocol**: `http/protobuf`
- **Endpoints**: Grafana Cloud OTLP Gateway
- **Signals**: Traces, Metrics, Logs
- **Export**: Batch processors with 60s interval

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/DaveOzz14/ecommerce_python.git
cd ecommerce_python
git checkout app_otel
```

2. **Create virtual environment**:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure OTLP** (`.env` already exists with credentials):
```bash
# Verify .env contains:
# - OTEL_EXPORTER_OTLP_ENDPOINT
# - OTEL_EXPORTER_OTLP_HEADERS (Authorization token)
# - OTEL_SERVICE_NAME
```

5. **Run the application**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Usage

1. Navigate to `http://localhost:8000`
2. Login with any username
3. View products catalog
4. Select a product to checkout

**All actions generate telemetry**:
- HTTP requests → Automatic traces
- Business actions → Manual spans with attributes
- Logs → Correlated with trace/span IDs
- Metrics → HTTP RED metrics exported

## Telemetry Validation

After starting the app, verify telemetry export:

1. **Check logs** for OpenTelemetry initialization
2. **Grafana Cloud**: Navigate to Explore → Tempo/Loki/Prometheus
3. **Query traces**: `{resource.service.name="ecommerce-python"}`
4. **Query logs**: `{service_name="ecommerce-python"}`
5. **Query metrics**: `http_server_request_duration_milliseconds`

## Manual Spans

Each router includes business-level spans:

- **Login**: `user_login` with `user.name` attribute
- **Products**: `view_product_catalog` with `product.count`
- **Checkout**: `checkout_product` with `product.id`, `product.name`, `product.price`

All spans include:
- Error status on exceptions
- Exception recording
- Business attributes
- Proper parent-child context

## Dependencies

```txt
fastapi==0.115.6
uvicorn==0.34.0
jinja2==3.1.5
python-multipart==0.0.20
opentelemetry-api==1.29.0
opentelemetry-sdk==1.29.0
opentelemetry-exporter-otlp-proto-http==1.29.0
opentelemetry-instrumentation-fastapi==0.50b0
opentelemetry-instrumentation-logging==0.50b0
python-dotenv==1.0.1
```

## Troubleshooting

**No telemetry exported?**
1. Verify `.env` configuration
2. Check OTLP endpoint connectivity
3. Validate authorization token
4. Review application logs for export errors

**Traces not correlated with logs?**
- Ensure `LoggingInstrumentor` is initialized
- Check `LoggingHandler` is attached to root logger

**Metrics not appearing?**
- Wait 60 seconds for first export (batch processor interval)
- Verify `MeterProvider` initialization

## Production Deployment

1. **Never commit `.env`** with real credentials
2. Use environment variables or secrets management
3. Configure appropriate batch processor intervals
4. Monitor OTLP exporter performance
5. Set proper resource attributes (region, instance, etc.)

## Support

For issues or questions about OpenTelemetry instrumentation, refer to:
- [OpenTelemetry Python Docs](https://opentelemetry.io/docs/instrumentation/python/)
- [Grafana Cloud OTLP Integration](https://grafana.com/docs/grafana-cloud/monitor-applications/application-observability/setup/collector/otlp/)
