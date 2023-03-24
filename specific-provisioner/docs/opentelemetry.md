# OpenTelemetry Instrumentation
 [OpenTelemetry](https://opentelemetry.io/docs/concepts/) is an observability framework designed to aid in the generation and collection of application telemetry data such as metrics, logs, and traces.



#### Setup Automatic Instrumentation
Automatic instrumentation uses a Python agent that can be attached to any Python application. It dynamically injects bytecode to capture telemetry from many popular libraries and frameworks. This reduces the amount of work required to integrate OpenTelemetry into the application code.

The appropriate Python packages for the automatic instrumentation have already been included in the `pyproject.toml`.

The agent is highly configurable (see [doc](https://opentelemetry.io/docs/instrumentation/python/automatic/agent-config/)). Here’s an example of agent configuration via environment variables:
```
OTEL_SERVICE_NAME=your-service-name \
OTEL_TRACES_EXPORTER=console,otlp \
OTEL_METRICS_EXPORTER=console \
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=0.0.0.0:4317 \
opentelemetry-instrument \
uvicorn src.main:app --host localhost --port 5002
```
Here’s an explanation of what each environment variables does:
- `OTEL_SERVICE_NAME`  sets the name of the service associated with your telemetry, and is sent to your [Observability backend](https://opentelemetry.io/ecosystem/vendors/).
- `OTEL_TRACES_EXPORTER` specifies which traces exporter to use. In this case, traces are being exported to `console` (stdout) and with `otlp`.
- `OTEL_METRICS_EXPORTER` specifies which metrics exporter to use. In this case, metrics are being exported to `console` (stdout).
- `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` sets the endpoint where telemetry is exported to. If omitted, the default `Collector` endpoint will be used, which is `0.0.0.0:4317` for gRPC and `0.0.0.0:4318` for HTTP.

#### Setup SigNoz as osservability backend
One of the biggest advantages of using OpenTelemetry is that it is vendor-agnostic. It can export data in multiple formats which you can send to a backend of your choice.

As osservability backend we will refer to [SigNoz](https://signoz.io/). SigNoz is an open-source APM tool that can be used for both metrics and distributed tracing.

##### 1. Installation using Docker Compose
> **Note**
Before you install SigNoz, ensure that [Docker Compose](https://docs.docker.com/compose/) is installed on your machine.

1. In a directory of your choosing, clone the SigNoz repository and `cd` into the `signoz/deploy` directory by entering the following commands:
```
git clone -b main https://github.com/SigNoz/signoz.git && cd signoz/deploy/
```
2. To install SigNoz, enter the `docker-compose up` command, specifying the following:
- `-f` and the path to your configuration file
- `-d` to run containers in the background.
```
docker-compose -f docker/clickhouse-setup/docker-compose.yaml up -d
```

For detailed instructions, you can visit the official documentation [here](https://signoz.io/docs/install/docker/?utm_source=blog&utm_medium=fastapi).

When you are done installing SigNoz, you can access the UI at `http://<IP-ADDRESS>:3301/`, replacing <IP-ADDRESS> with the `<IP address>` of the machine where you installed SigNoz.
> If you are running SigNoz on your local machine, you should point your browser to [http://localhost:3301/](http://localhost:3301/).

The application list shown in the dashboard is from a sample app called HOT R.O.D that comes bundled with the SigNoz installation package.
##### 2. Sending Data
You just need to configure a few environment variables for your OTLP exporters. Environment variables that need to be configured:
- `service.name` - application service name (you can name it as you like).
- `OTEL_EXPORTER_OTLP_ENDPOINT`- in this case, IP of the machine where SigNoz is installed.

You need to put these environment variables in the below command:
```
OTEL_RESOURCE_ATTRIBUTES=service.name=<service_name> OTEL_EXPORTER_OTLP_ENDPOINT="http://<IP of SigNoz>:4317" opentelemetry-instrument uvicorn src.main:app --host localhost --port 5002
```
If you are running SigNoz on local host, `IP of SigNoz` can be replaced with `localhost` in this case. And, for `service_name` let's use `PythonSpecificProvisioner`. Hence, the final command becomes:
```
OTEL_RESOURCE_ATTRIBUTES=service.name=PythonSpecificProvisioner OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317" opentelemetry-instrument uvicorn src.main:app --host localhost --port 5002
```
You can check if your app is running or not by hitting the endpoint at [http://localhost:5002](http://localhost:5002/).

If you have installed SigNoz on your local host, then you can access the SigNoz dashboard at [http://localhost:3301](http://localhost:3301) to monitor your app for performance metrics.
