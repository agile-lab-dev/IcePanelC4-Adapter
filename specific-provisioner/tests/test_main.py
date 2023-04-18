from src.main import provision
from src.models import DescriptorKind, ProvisioningRequest


def test_one():
    assert True is True


def test_add():
    provisioning_request = ProvisioningRequest(
        descriptorKind=DescriptorKind.COMPONENT_DESCRIPTOR, descriptor="prova"
    )
    provision(provisioning_request)
    assert 1 + 1 == 2
