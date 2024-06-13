from __future__ import annotations

from requests.auth import HTTPBasicAuth
import requests

import sys
import os

import yaml
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

import asyncio 


from src.dependencies import unpack_provisioning_request
from src.utility.parsing_pydantic_models import parse_yaml_with_model

from starlette.responses import Response

from src.app_config import app
from src.check_return_type import check_response
from src.models.api_models import (
    ProvisioningRequest,
    ProvisioningStatus,
    SystemErr,
    UpdateAclRequest,
    ValidationError,
    ValidationRequest,
    ValidationResult,
    ValidationStatus,
)

from src.models.icepanel import *
from src.models.data_product_descriptor import *

from src.utility.logger import get_logger

logger = get_logger()


@app.post(
    "/v1/provision",
    response_model=None,
    responses={
        "200": {"model": ProvisioningStatus},
        "202": {"model": str},
        "400": {"model": ValidationError},
        "500": {"model": SystemErr},
    },
    tags=["SpecificProvisioner"],
)
async def provision(
    body: ProvisioningRequest,
) -> Response:
    """
    Deploy a data product or a single component starting from a provisioning descriptor
    """

    # get data from icepanel
    (domains, modelObjects, modelConnections) = getIcePanelSituation()
    
    dp = await unpack_provisioning_request(body)
    print("------------------DESCRIPTOR PARSED-----------------------------")
    print(dp)

    # default domain in the organization data mesh and landscape [hWFggyCYwu5kun6fpsu7]
    domainId= list(filter(lambda x: x.name == "Default domain", domains))[0].id
    rootId=list(filter(lambda x: x.type == "root", modelObjects))[0].id
   
    icePanelDP = dp[0].toIcePanel(domainId, rootId)
    
    matchedDP = list(filter(lambda x: x.name == icePanelDP.name, modelObjects))
    dpId: str = ""
    if len(matchedDP) == 1:
        dpId = patch_component(matchedDP[0].id, icePanelDP)

    else:
        dpId = post_component(icePanelDP)    

    
    witboostCompToIcePanelComp: dict[str,str] = {}
    for component in dp[0].components:
        cdict: dict = component.dict()
        icePanelObj = component.toIcePanel(domainId,dpId)
        
        if not icePanelObj == None:
            matchedComponent = list(filter(lambda x: x.name == icePanelObj.name, modelObjects))
            compId = ""
            if len(matchedComponent) == 1:
                compId = patch_component(matchedComponent[0].id, icePanelObj)                
            else:
                compId = post_component(icePanelObj)                

            witboostCompToIcePanelComp[component.id] = compId

    for component in dp[0].components:
        print("component type: " + str(component.kind))
        cdict: dict = component.dict()

        dependsOn = []
        readsFrom = []
        if component.kind == "outputport":
            rename_key(cdict['dataContract'], 'schema_', 'schema')
            outputport = OutputPort(**cdict)
            dependsOn = outputport.dependsOn

        if component.kind == "workload":
            workload = Workload(**cdict)
            dependsOn = workload.dependsOn
            readsFrom = workload.readsFrom
        
        processRelationships(component, dependsOn, dp[0].components, "dependsOn", witboostCompToIcePanelComp, modelConnections )
        processRelationships(component, readsFrom, dp[0].components, "readsFrom", witboostCompToIcePanelComp, modelConnections )

    resp = SystemErr(error="Response not yet implemented")

    return check_response(out_response=resp)

def processRelationships(currComponent, relationships, components, relationshipType, witboostCompToIcePanelComp, existingConnections):
    if len(relationships) > 0:
        for relID in relationships:
            for relaedComp in components:
                if relaedComp.id == relID:
                    connection = buildConnection(relationshipType, witboostCompToIcePanelComp[currComponent.id], witboostCompToIcePanelComp[relaedComp.id])

                    matchedConnection = list(filter(lambda x: x.originId == connection.originId and x.targetId == connection.targetId and x.name == relationshipType, existingConnections))
                    if len(matchedConnection) == 1:
                        compId = patch_connection(matchedConnection[0].id, connection)     
                    else:
                        compId = post_connection(connection)

def rename_key(dictionary, old_key, new_key):
    if old_key in dictionary:
        dictionary[new_key] = dictionary.pop(old_key)
    else:
        raise KeyError(f"Key '{old_key}' not found in dictionary")

@app.get(
    "/v1/provision/{token}/status",
    response_model=None,
    responses={
        "200": {"model": ProvisioningStatus},
        "400": {"model": ValidationError},
        "500": {"model": SystemErr},
    },
    tags=["SpecificProvisioner"],
)
def get_status(token: str) -> Response:
    """
    Get the status for a provisioning request
    """



    # todo: define correct response
    resp = SystemErr(error="Response not yet implemented")

    return check_response(out_response=resp)


@app.post(
    "/v1/unprovision",
    response_model=None,
    responses={
        "200": {"model": ProvisioningStatus},
        "202": {"model": str},
        "400": {"model": ValidationError},
        "500": {"model": SystemErr},
    },
    tags=["SpecificProvisioner"],
)
def unprovision(
    body: ProvisioningRequest,
) -> Response:
    """
    Undeploy a data product or a single component
    given the provisioning descriptor relative to the latest complete provisioning request
    """  # noqa: E501

    # todo: define correct response
    resp = SystemErr(error="Response not yet implemented")

    return check_response(out_response=resp)


@app.post(
    "/v1/updateacl",
    response_model=None,
    responses={
        "200": {"model": ProvisioningStatus},
        "202": {"model": str},
        "400": {"model": ValidationError},
        "500": {"model": SystemErr},
    },
    tags=["SpecificProvisioner"],
)
def updateacl(
    body: UpdateAclRequest,
) -> Response:
    """
    Request the access to a specific provisioner component
    """

    # todo: define correct response
    resp = SystemErr(error="Response not yet implemented")

    return check_response(out_response=resp)


@app.post(
    "/v1/validate",
    response_model=None,
    responses={"200": {"model": ValidationResult}, "500": {"model": SystemErr}},
    tags=["SpecificProvisioner"],
)
def validate(body: ProvisioningRequest) -> Response:
    """
    Validate a provisioning request
    """

    # todo: define correct response
    resp = SystemErr(error="Response not yet implemented")

    return check_response(out_response=resp)


@app.post(
    "/v2/validate",
    response_model=None,
    responses={
        "202": {"model": str},
        "400": {"model": ValidationError},
        "500": {"model": SystemErr},
    },
    tags=["SpecificProvisioner"],
)
def async_validate(
    body: ValidationRequest,
) -> Response:
    """
    Validate a deployment request
    """

    # todo: define correct response
    resp = SystemErr(error="Response not yet implemented")

    return check_response(out_response=resp)


@app.get(
    "/v2/validate/{token}/status",
    response_model=None,
    responses={
        "200": {"model": ValidationStatus},
        "400": {"model": ValidationError},
        "500": {"model": SystemErr},
    },
    tags=["SpecificProvisioner"],
)
def get_validation_status(
    token: str,
) -> Response:
    """
    Get the status for a provisioning request
    """

    # todo: define correct response
    resp = SystemErr(error="Response not yet implemented")

    return check_response(out_response=resp)
