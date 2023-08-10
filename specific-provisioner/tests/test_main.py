from starlette.testclient import TestClient

from src.main import app
from src.models import DescriptorKind, ProvisioningRequest

client = TestClient(app)


def test_provisioning():
    provisioning_request = ProvisioningRequest(
        descriptorKind=DescriptorKind.COMPONENT_DESCRIPTOR, descriptor="descriptor"
    )

    resp = client.post("/v1/provision", json=dict(provisioning_request))

    assert 'Response not yet implemented' in resp.json().get('error')


def test_unprovisioning():
    provisioning_request = ProvisioningRequest(
        descriptorKind=DescriptorKind.COMPONENT_DESCRIPTOR, descriptor="descriptor"
    )

    resp = client.post("/v1/unprovision", json=dict(provisioning_request))

    assert 'Response not yet implemented' in resp.json().get('error')
