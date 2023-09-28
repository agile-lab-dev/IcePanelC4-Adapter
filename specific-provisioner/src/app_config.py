from fastapi import FastAPI

app = FastAPI(
    title="Specific Provisioner Micro Service",
    description="Microservice responsible to handle provisioning and access control requests for one or more data product components.",  # noqa: E501
    version="{{version}}",
    servers=[{"url": "/datamesh.specificprovisioner"}],
)
