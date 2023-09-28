import unittest
from unittest.mock import Mock

from fastapi import FastAPI
from starlette.testclient import TestClient

from src.dependencies import (
    UnpackedProvisioningRequestDep,
    UnpackedUpdateAclRequestDep,
    unpack_provisioning_request,
    unpack_update_acl_request,
)
from src.models.api_models import (
    ProvisionInfo,
    ProvisioningRequest,
    UpdateAclRequest,
    ValidationError,
)
from src.models.data_product_descriptor import DataProduct


class TestUnpackUpdateAclRequest(unittest.TestCase):
    update_acl_request = UpdateAclRequest(
        refs=["user:testuser", "bigData"],
        provisionInfo=ProvisionInfo(
            request="""
            dataProduct:
              id: data_product_123
              name: My Data Product
              description: This is a sample Data Product for testing purposes.
              kind: dataproduct
              domain: example.com
              version: '1.0'
              environment: production
              dataProductOwner: John Doe
              ownerGroup: data_product_owners
              devGroup: data_product_devs
              tags:
              - tagFQN: data_product_tag1
              - tagFQN: data_product_tag2
              specific:
                customField1: Value1
                customField2: Value2
              components:
              - id: component1
                name: Component 1
                description: This is the first component.
                kind: outputport
                version: '1.0'
                infrastructureTemplateId: infrastructure_template_1
                specific:
                  outputPortSpecificField1: OutputPortValue1
                  outputPortSpecificField2: OutputPortValue2
              - id: component2
                name: Component 2
                description: This is the second component.
                kind: outputport
                version: '1.0'
                infrastructureTemplateId: infrastructure_template_2
                specific:
                  outputPortSpecificField1: val3
                  outputPortSpecificField2: val4
            componentIdToProvision: id123

            """,  # noqa: E501
            result="result_prov",
        ),
    )

    async def test_successful_unpack(self):
        result = unpack_update_acl_request(self.update_acl_request)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], DataProduct)
        self.assertEqual(result[1], "id123")
        self.assertEqual(result[2], self.update_acl_request.refs)

    async def test_invalid_request(self):
        # Create a mock UpdateAclRequest instance with an invalid request
        update_acl_request = Mock()
        update_acl_request.provisionInfo.request = 'Invalid JSON'

        # Call the function and assert the result
        result = unpack_update_acl_request(update_acl_request)
        self.assertIsInstance(result, ValidationError)
        self.assertIn("Unable to parse the descriptor.", result.errors[0])

    async def test_exception_handling(self):
        update_acl_request = Mock()
        update_acl_request.provisionInfo.request = '{}'

        result = unpack_update_acl_request(update_acl_request)
        self.assertIsInstance(result, ValidationError)


class TestUnpackProvisioningRequest(unittest.TestCase):
    provisioning_request = ProvisioningRequest(
        descriptorKind="COMPONENT_DESCRIPTOR",
        descriptor="""
                dataProduct:
                  id: data_product_123
                  name: My Data Product
                  description: This is a sample Data Product for testing purposes.
                  kind: dataproduct
                  domain: example.com
                  version: '1.0'
                  environment: production
                  dataProductOwner: John Doe
                  ownerGroup: data_product_owners
                  devGroup: data_product_devs
                  tags:
                  - tagFQN: data_product_tag1
                  - tagFQN: data_product_tag2
                  specific:
                    customField1: Value1
                    customField2: Value2
                  components:
                  - id: component1
                    name: Component 1
                    description: This is the first component.
                    kind: outputport
                    version: '1.0'
                    infrastructureTemplateId: infrastructure_template_1
                    specific:
                      outputPortSpecificField1: OutputPortValue1
                      outputPortSpecificField2: OutputPortValue2
                  - id: component2
                    name: Component 2
                    description: This is the second component.
                    kind: outputport
                    version: '1.0'
                    infrastructureTemplateId: infrastructure_template_2
                    specific:
                      outputPortSpecificField1: val3
                      outputPortSpecificField2: val4
                componentIdToProvision: id123
        """,  # noqa: E501
    )

    invalid_provisioning_request = ProvisioningRequest(
        # dropped the 'name' field from the previous provisioning_request
        descriptorKind="COMPONENT_DESCRIPTOR",
        descriptor="""
        dataProduct:
          id: data_product_123
          description: This is a sample Data Product for testing purposes.
          kind: dataproduct
          domain: example.com
          version: '1.0'
          environment: production
          dataProductOwner: John Doe
          ownerGroup: data_product_owners
          devGroup: data_product_devs
          tags:
          - tagFQN: data_product_tag1
          - tagFQN: data_product_tag2
          specific:
            customField1: Value1
            customField2: Value2
          components:
          - id: component1
            name: Component 1
            description: This is the first component.
            kind: outputport
            version: '1.0'
            infrastructureTemplateId: infrastructure_template_1
            specific:
              outputPortSpecificField1: OutputPortValue1
              outputPortSpecificField2: OutputPortValue2
          - id: component2
            name: Component 2
            description: This is the second component.
            kind: outputport
            version: '1.0'
            infrastructureTemplateId: infrastructure_template_2
            specific:
              outputPortSpecificField1: val3
              outputPortSpecificField2: val4
        componentIdToProvision: id123
        """,  # noqa: E501
    )

    async def test_successful_unpack(self):
        result = unpack_provisioning_request(self.provisioning_request)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], DataProduct)
        self.assertEqual(result[1], "id123")

    async def test_invalid_request(self):
        result = unpack_provisioning_request(self.invalid_provisioning_request)
        self.assertIsInstance(result, ValidationError)
        self.assertIn("An error occurred parsing the yaml data with", result.errors[0])

    async def test_exception_handling(self):
        provisioning_request = Mock()
        provisioning_request.descriptorKind = "COMPONENT_DESCRIPTOR"
        provisioning_request.descriptor = 'Invalid JSON'

        result = unpack_provisioning_request(provisioning_request)
        self.assertIsInstance(result, ValidationError)


app_test = FastAPI()


@app_test.post("/provision")
async def provision(data: UnpackedProvisioningRequestDep):
    if isinstance(data, tuple) and len(data) == 2:
        data_product, component_id = data
        return {
            "message": "Provisioning completed successfully",
            "data_product": data_product,
            "component_id": component_id,
        }
    elif isinstance(data, ValidationError):
        return {"message": "Provisioning failed", "errors": data.errors}


@app_test.post("/updateacl")
async def update_acl(data: UnpackedUpdateAclRequestDep):
    if isinstance(data, tuple) and len(data) == 3:
        data_product, component_id, refs = data
        return {
            "message": "Update acl completed successfully",
            "data_product": data_product,
            "component_id": component_id,
        }
    elif isinstance(data, ValidationError):
        return {"message": "Provisioning failed", "errors": data.errors}


client = TestClient(app_test)


class TestAppDependenciesMock(unittest.TestCase):
    def test_provision_valid_request(self):
        valid_provisioning_request = ProvisioningRequest(
            descriptorKind="COMPONENT_DESCRIPTOR",
            descriptor="""
            dataProduct:
              id: data_product_123
              name: My Data Product
              description: This is a sample Data Product for testing purposes.
              kind: dataproduct
              domain: example.com
              version: '1.0'
              environment: production
              dataProductOwner: John Doe
              ownerGroup: data_product_owners
              devGroup: data_product_devs
              tags:
              - tagFQN: data_product_tag1
              - tagFQN: data_product_tag2
              specific:
                customField1: Value1
                customField2: Value2
              components:
              - id: component1
                name: Component 1
                description: This is the first component.
                kind: outputport
                version: '1.0'
                infrastructureTemplateId: infrastructure_template_1
                specific:
                  outputPortSpecificField1: OutputPortValue1
                  outputPortSpecificField2: OutputPortValue2
              - id: component2
                name: Component 2
                description: This is the second component.
                kind: outputport
                version: '1.0'
                infrastructureTemplateId: infrastructure_template_2
                specific:
                  outputPortSpecificField1: val3
                  outputPortSpecificField2: val4
            componentIdToProvision: id123
            """,  # noqa: E501
        )

        response = client.post(
            "/provision", json=valid_provisioning_request.model_dump()
        )

        assert response.status_code == 200
        assert "Provisioning completed successfully" in response.json()["message"]
        assert "data_product" in response.json()
        assert "component_id" in response.json()

    def test_provision_invalid_request(self):
        invalid_provisioning_request = ProvisioningRequest(
            descriptorKind="COMPONENT_DESCRIPTOR", descriptor="invalid_descriptor"
        )

        response = client.post(
            "/provision", json=invalid_provisioning_request.model_dump()
        )

        assert response.status_code == 200
        assert "Provisioning failed" in response.json()["message"]
        assert "errors" in response.json()

    def test_updateacl_valid_request(self):
        valid_update_acl_request = UpdateAclRequest(
            refs=["user:testuser", "bigData"],
            provisionInfo=ProvisionInfo(
                request="""
                dataProduct:
                  id: data_product_123
                  name: My Data Product
                  description: This is a sample Data Product for testing purposes.
                  kind: dataproduct
                  domain: example.com
                  version: '1.0'
                  environment: production
                  dataProductOwner: John Doe
                  ownerGroup: data_product_owners
                  devGroup: data_product_devs
                  tags:
                  - tagFQN: data_product_tag1
                  - tagFQN: data_product_tag2
                  specific:
                    customField1: Value1
                    customField2: Value2
                  components:
                  - id: component1
                    name: Component 1
                    description: This is the first component.
                    kind: outputport
                    version: '1.0'
                    infrastructureTemplateId: infrastructure_template_1
                    specific:
                      outputPortSpecificField1: OutputPortValue1
                      outputPortSpecificField2: OutputPortValue2
                  - id: component2
                    name: Component 2
                    description: This is the second component.
                    kind: outputport
                    version: '1.0'
                    infrastructureTemplateId: infrastructure_template_2
                    specific:
                      outputPortSpecificField1: val3
                      outputPortSpecificField2: val4
                componentIdToProvision: id123

                """,  # noqa: E501
                result="result_prov",
            ),
        )

        response = client.post("/updateacl", json=valid_update_acl_request.model_dump())

        assert response.status_code == 200
        assert "Update acl completed successfully" in response.json()["message"]
        assert "data_product" in response.json()
        assert "component_id" in response.json()

    def test_updateacl_invalid_request(self):
        invalid_provisioning_request = UpdateAclRequest(
            refs=["user:testuser", "bigData"],
            provisionInfo=ProvisionInfo(
                request="invalid_request",
                result="result_prov",
            ),
        )

        response = client.post(
            "/updateacl", json=invalid_provisioning_request.model_dump()
        )

        assert response.status_code == 200
        assert "Provisioning failed" in response.json()["message"]
        assert "errors" in response.json()
