from typing import Dict, List, Optional, Union
from pydantic import BaseModel
import json

import sys
import os

from requests.auth import HTTPBasicAuth
import requests
import yaml

from starlette.responses import Response
import asyncio 

from src.utility.parsing_pydantic_models import parse_yaml_with_model

landscapeId = os.getenv('IcePanelLandscapeId')
apiKey = os.getenv('API_KEY')
headers = {'Accept': 'application/json', 'Authorization': f'ApiKey {apiKey}'}
print(headers)

class Domain(BaseModel):
    id: str
    name: str

class Flow(BaseModel):
    pass  # Add fields as necessary

class ModelConnection(BaseModel):
    description: str
    direction: str
    id: str
    name: str
    originId: str
    status: str
    tagIds: List[str]
    targetId: str
    technologies: Dict[str, Optional[str]]

class ModelObject(BaseModel):
    caption: str
    description: str
    domainId: str
    external: bool
    icon: Optional[str]
    id: str
    links: Dict[str, str]
    name: str
    parentId: Optional[str]
    parentIds: List[str]
    status: str
    tagIds: List[str]
    teamIds: List[str]
    technologies: Dict[str, str]
    type: str

class TagGroup(BaseModel):
    icon: str
    id: str
    name: str

class Tag(BaseModel):
    color: str
    groupId: str
    id: str
    name: str

class Team(BaseModel):
    pass  # Add fields as necessary

class IcePanelData(BaseModel):
    domains: Dict[str, Domain]
    flows: Dict[str, Flow]
    modelConnections: Dict[str, ModelConnection]
    modelObjects: Dict[str, ModelObject]
    tagGroups: Dict[str, TagGroup]
    tags: Dict[str, Tag]
    teams: Dict[str, Team]





def buildConnection(type, source, target):
    return ModelConnection(
                            description=type,
                            direction="outgoing",
                            id="",
                            name=type,
                            originId= source,
                            status="live",
                            tagIds=[], 
                            targetId = target,
                            technologies={}
    )

def patch_connection(conn_id, connection):
    return patch(connection.dict(), "connections", conn_id)

def patch_component(comp_id, component) -> str:
    return patch(component.dict(), "objects", comp_id)

def post_connection(connection):
    return post(connection.dict(), "connections")

def post_component(component) -> str:
    return post(component.dict(), "objects")

def patch(objectDict, objectType, objId) -> str:
    
    patch_url = f'https://api.icepanel.io/v1/landscapes/{landscapeId}/versions/latest/model/{objectType}/{objId}'
    data = objectDict
    print("----------------------------")
    print(data)
    response = requests.patch(patch_url, json=data, headers=headers)
    print(response.content)
    response.raise_for_status()
    print(response.content)
    return objId

def post(objectDict, objectType) -> str:
    post_url = f'https://api.icepanel.io/v1/landscapes/{landscapeId}/versions/latest/model/{objectType}'
    data = objectDict
    response = requests.post(post_url, json=data, headers=headers)
    response.raise_for_status()
    created_object = yaml.safe_load(response.content)
    modelType = "modelConnection"
    if objectType == "objects":
        modelType = "modelObject"
    created_id = created_object.get(modelType).get("id")
    print(created_id)
    return created_id

def getIcePanelSituation():
    exportUrl = f'https://api.icepanel.io/v1/landscapes/{landscapeId}/versions/latest/export/json'
    
    response = requests.get(exportUrl, headers=headers)
    print(response.content)
    # Parse the JSON string
    yamlparsed: dict = yaml.safe_load(response.content)
    icepanel_response = parse_yaml_with_model(yamlparsed, IcePanelData)
    print(icepanel_response)
    return (icepanel_response.domains.values(), icepanel_response.modelObjects.values(), icepanel_response.modelConnections.values())
    