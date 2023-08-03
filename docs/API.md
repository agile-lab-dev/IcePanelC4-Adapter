
<!-- Generator: Widdershins v4.0.1 -->

<h1 id="specific-provisioner-micro-service">Specific Provisioner Micro Service</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

Microservice responsible to handle provisioning and access control requests for one or more data product components.

<h1 id="specific-provisioner-micro-service-specificprovisioner">SpecificProvisioner</h1>

All the provisioning related operations

## asyncValidate

<a id="opIdasyncValidate"></a>

### Code samples

<details>
  <summary>Shell</summary>

```shell
# You can also use wget
curl -X POST /v2/validate \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```
</details>

<details>
  <summary>JavaScript</summary>

```javascript
const inputBody = '{
  "descriptor": "string"
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json'
};

fetch('/v2/validate',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```
</details>

<details>
  <summary>Java</summary>

```java
URL obj = new URL("/v2/validate");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```
</details>

<details>
  <summary>Python</summary>

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/v2/validate', headers = headers)

print(r.json())

```
</details>

`POST /v2/validate`

*Validate a deployment request*

> Body parameter

```json
{
  "descriptor": "string"
}
```

<h3 id="asyncvalidate-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[ValidationRequest](#schemavalidationrequest)|true|A deployment request descriptor wrapped as a string into a simple object|

> Example responses

> 202 Response

```json
"string"
```

<h3 id="asyncvalidate-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|Returns the DAG id of the Provisioning Plan|string|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid input|[ValidationError](#schemavalidationerror)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|System problem|[SystemError](#schemasystemerror)|

<aside class="success">
This operation does not require authentication
</aside>

## getValidationStatus

<a id="opIdgetValidationStatus"></a>

### Code samples

<details>
  <summary>Shell</summary>

```shell
# You can also use wget
curl -X GET /v2/validate/{token}/status \
  -H 'Accept: application/json'

```
</details>

<details>
  <summary>JavaScript</summary>

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('/v2/validate/{token}/status',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```
</details>

<details>
  <summary>Java</summary>

```java
URL obj = new URL("/v2/validate/{token}/status");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```
</details>

<details>
  <summary>Python</summary>

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/v2/validate/{token}/status', headers = headers)

print(r.json())

```
</details>

`GET /v2/validate/{token}/status`

*Get the status for a provisioning request*

<h3 id="getvalidationstatus-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|token|path|string|true|token that identifies the request|

> Example responses

> 200 Response

```json
{
  "status": "RUNNING",
  "result": {
    "valid": true,
    "error": {
      "errors": [
        "string"
      ]
    }
  }
}
```

<h3 id="getvalidationstatus-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|The request status|[ValidationStatus](#schemavalidationstatus)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid input|[ValidationError](#schemavalidationerror)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|System problem|[SystemError](#schemasystemerror)|

<aside class="success">
This operation does not require authentication
</aside>

## provision

<a id="opIdprovision"></a>

### Code samples

<details>
  <summary>Shell</summary>

```shell
# You can also use wget
curl -X POST /v1/provision \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```
</details>

<details>
  <summary>JavaScript</summary>

```javascript
const inputBody = '{
  "descriptorKind": "DATAPRODUCT_DESCRIPTOR",
  "descriptor": "string"
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json'
};

fetch('/v1/provision',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```
</details>

<details>
  <summary>Java</summary>

```java
URL obj = new URL("/v1/provision");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```
</details>

<details>
  <summary>Python</summary>

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/v1/provision', headers = headers)

print(r.json())

```
</details>

`POST /v1/provision`

*Deploy a data product or a single component starting from a provisioning descriptor*

> Body parameter

```json
{
  "descriptorKind": "DATAPRODUCT_DESCRIPTOR",
  "descriptor": "string"
}
```

<h3 id="provision-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[ProvisioningRequest](#schemaprovisioningrequest)|true|Provisioning descriptor|

> Example responses

> 200 Response

```json
{
  "status": "RUNNING",
  "result": "string",
  "info": {
    "publicInfo": {},
    "privateInfo": {}
  }
}
```

<h3 id="provision-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|It synchronously returns the request result|[ProvisioningStatus](#schemaprovisioningstatus)|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|If successful returns a provisioning deployment task token that can be used for polling the request status|string|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid input|[ValidationError](#schemavalidationerror)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|System problem|[SystemError](#schemasystemerror)|

<aside class="success">
This operation does not require authentication
</aside>

## getStatus

<a id="opIdgetStatus"></a>

### Code samples

<details>
  <summary>Shell</summary>

```shell
# You can also use wget
curl -X GET /v1/provision/{token}/status \
  -H 'Accept: application/json'

```
</details>

<details>
  <summary>JavaScript</summary>

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('/v1/provision/{token}/status',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```
</details>

<details>
  <summary>Java</summary>

```java
URL obj = new URL("/v1/provision/{token}/status");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("GET");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```
</details>

<details>
  <summary>Python</summary>

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/v1/provision/{token}/status', headers = headers)

print(r.json())

```
</details>

`GET /v1/provision/{token}/status`

*Get the status for a provisioning request*

<h3 id="getstatus-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|token|path|string|true|token that identifies the request|

> Example responses

> 200 Response

```json
{
  "status": "RUNNING",
  "result": "string",
  "info": {
    "publicInfo": {},
    "privateInfo": {}
  }
}
```

<h3 id="getstatus-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|The request status|[ProvisioningStatus](#schemaprovisioningstatus)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid input|[ValidationError](#schemavalidationerror)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|System problem|[SystemError](#schemasystemerror)|

<aside class="success">
This operation does not require authentication
</aside>

## validate

<a id="opIdvalidate"></a>

### Code samples

<details>
  <summary>JavaScript</summary>

```shell
# You can also use wget
curl -X POST /v1/validate \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```
</details>

<details>
  <summary>JavaScript</summary>

```javascript
const inputBody = '{
  "descriptorKind": "DATAPRODUCT_DESCRIPTOR",
  "descriptor": "string"
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json'
};

fetch('/v1/validate',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```
</details>

<details>
  <summary>Java</summary>

```java
URL obj = new URL("/v1/validate");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```
</details>

<details>
  <summary>Python</summary>

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/v1/validate', headers = headers)

print(r.json())

```
</details>

`POST /v1/validate`

*Validate a provisioning request*

> Body parameter

```json
{
  "descriptorKind": "DATAPRODUCT_DESCRIPTOR",
  "descriptor": "string"
}
```

<h3 id="validate-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[ProvisioningRequest](#schemaprovisioningrequest)|true|Provisioning descriptor to be validated|

> Example responses

> 200 Response

```json
{
  "valid": true,
  "error": {
    "errors": [
      "string"
    ]
  }
}
```

<h3 id="validate-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|It synchronously returns a specific reply containing the validation result|[ValidationResult](#schemavalidationresult)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|System problem|[SystemError](#schemasystemerror)|

<aside class="success">
This operation does not require authentication
</aside>

## unprovision

<a id="opIdunprovision"></a>

### Code samples

<details>
  <summary>Shell</summary>

```shell
# You can also use wget
curl -X POST /v1/unprovision \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```
</details>

<details>
  <summary>JavaScript</summary>

```javascript
const inputBody = '{
  "descriptorKind": "DATAPRODUCT_DESCRIPTOR",
  "descriptor": "string"
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json'
};

fetch('/v1/unprovision',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```
</details>

<details>
  <summary>Java</summary>

```java
URL obj = new URL("/v1/unprovision");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```
</details>

<details>
  <summary>Python</summary>

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/v1/unprovision', headers = headers)

print(r.json())

```
</details>

`POST /v1/unprovision`

*Undeploy a data product or a single component given the provisioning descriptor relative to the latest complete provisioning request*

> Body parameter

```json
{
  "descriptorKind": "DATAPRODUCT_DESCRIPTOR",
  "descriptor": "string"
}
```

<h3 id="unprovision-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[ProvisioningRequest](#schemaprovisioningrequest)|true|Provisioning descriptor|

> Example responses

> 200 Response

```json
{
  "status": "RUNNING",
  "result": "string",
  "info": {
    "publicInfo": {},
    "privateInfo": {}
  }
}
```

<h3 id="unprovision-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|It synchronously returns the request result|[ProvisioningStatus](#schemaprovisioningstatus)|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|If successful returns a provisioning deployment task token that can be used for polling the request status|string|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid input|[ValidationError](#schemavalidationerror)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|System problem|[SystemError](#schemasystemerror)|

<aside class="success">
This operation does not require authentication
</aside>

## updateacl

<a id="opIdupdateacl"></a>

### Code samples

<details>
  <summary>Shell</summary>

```shell
# You can also use wget
curl -X POST /v1/updateacl \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json'

```
</details>

<details>
  <summary>JavaScript</summary>

```javascript
const inputBody = '{
  "refs": [
    "user:alice",
    "user:bob",
    "group:groupA",
    "group:groupB",
    "group:groupC"
  ],
  "provisionInfo": {
    "request": "string",
    "result": "string"
  }
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json'
};

fetch('/v1/updateacl',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```
</details>

<details>
  <summary>Java</summary>

```java
URL obj = new URL("/v1/updateacl");
HttpURLConnection con = (HttpURLConnection) obj.openConnection();
con.setRequestMethod("POST");
int responseCode = con.getResponseCode();
BufferedReader in = new BufferedReader(
    new InputStreamReader(con.getInputStream()));
String inputLine;
StringBuffer response = new StringBuffer();
while ((inputLine = in.readLine()) != null) {
    response.append(inputLine);
}
in.close();
System.out.println(response.toString());

```
</details>

<details>
  <summary>Python</summary>

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/v1/updateacl', headers = headers)

print(r.json())

```
</details>

`POST /v1/updateacl`

*Request the access to a specific provisioner component*

> Body parameter

```json
{
  "refs": [
    "user:alice",
    "user:bob",
    "group:groupA",
    "group:groupB",
    "group:groupC"
  ],
  "provisionInfo": {
    "request": "string",
    "result": "string"
  }
}
```

<h3 id="updateacl-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[UpdateAclRequest](#schemaupdateaclrequest)|true|An access request object. The provisoning info reported in `provisionInfo` refer to the latest complete provisioning workflow of the target component|

> Example responses

> 200 Response

```json
{
  "status": "RUNNING",
  "result": "string",
  "info": {
    "publicInfo": {},
    "privateInfo": {}
  }
}
```

<h3 id="updateacl-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|It synchronously returns the access request response|[ProvisioningStatus](#schemaprovisioningstatus)|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|If successful returns a provisioning deployment task token that can be used for polling the request status|string|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid input|[ValidationError](#schemavalidationerror)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|System problem|[SystemError](#schemasystemerror)|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_ValidationStatus">ValidationStatus</h2>
<!-- backwards compatibility -->
<a id="schemavalidationstatus"></a>
<a id="schema_ValidationStatus"></a>
<a id="tocSvalidationstatus"></a>
<a id="tocsvalidationstatus"></a>

```json
{
  "status": "RUNNING",
  "result": {
    "valid": true,
    "error": {
      "errors": [
        "string"
      ]
    }
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|status|string|true|none|none|
|result|[ValidationResult](#schemavalidationresult)|false|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|status|RUNNING|
|status|COMPLETED|
|status|FAILED|

<h2 id="tocS_ValidationRequest">ValidationRequest</h2>
<!-- backwards compatibility -->
<a id="schemavalidationrequest"></a>
<a id="schema_ValidationRequest"></a>
<a id="tocSvalidationrequest"></a>
<a id="tocsvalidationrequest"></a>

```json
{
  "descriptor": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|descriptor|string|true|none|none|

<h2 id="tocS_UpdateAclRequest">UpdateAclRequest</h2>
<!-- backwards compatibility -->
<a id="schemaupdateaclrequest"></a>
<a id="schema_UpdateAclRequest"></a>
<a id="tocSupdateaclrequest"></a>
<a id="tocsupdateaclrequest"></a>

```json
{
  "refs": [
    "user:alice",
    "user:bob",
    "group:groupA",
    "group:groupB",
    "group:groupC"
  ],
  "provisionInfo": {
    "request": "string",
    "result": "string"
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|refs|[string]|true|none|Identities (i.e. users and groups) involved in the ACL update request|
|provisionInfo|[ProvisionInfo](#schemaprovisioninfo)|true|none|Information related to the provisioning workflow of a data product component|

<h2 id="tocS_DescriptorKind">DescriptorKind</h2>
<!-- backwards compatibility -->
<a id="schemadescriptorkind"></a>
<a id="schema_DescriptorKind"></a>
<a id="tocSdescriptorkind"></a>
<a id="tocsdescriptorkind"></a>

```json
"DATAPRODUCT_DESCRIPTOR"

```

Values:
 * `DATAPRODUCT_DESCRIPTOR` - Complete descriptor of a data product. It is used in the data product level provisioning workflow.
 * `COMPONENT_DESCRIPTOR` - Provisioning descriptor for a single data product component. Includes both the complete data product descriptor (`dataProduct` object field) and the id of the component to be provisioned (`componentIdToProvision` string field).
 * `DATAPRODUCT_DESCRIPTOR_WITH_RESULTS` - This value is not currently used in the scope of a specific provisioner.

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|*anonymous*|string|false|none|Values:<br> * `DATAPRODUCT_DESCRIPTOR` - Complete descriptor of a data product. It is used in the data product level provisioning workflow.<br> * `COMPONENT_DESCRIPTOR` - Provisioning descriptor for a single data product component. Includes both the complete data product descriptor (`dataProduct` object field) and the id of the component to be provisioned (`componentIdToProvision` string field).<br> * `DATAPRODUCT_DESCRIPTOR_WITH_RESULTS` - This value is not currently used in the scope of a specific provisioner.|

#### Enumerated Values

|Property|Value|
|---|---|
|*anonymous*|DATAPRODUCT_DESCRIPTOR|
|*anonymous*|COMPONENT_DESCRIPTOR|
|*anonymous*|DATAPRODUCT_DESCRIPTOR_WITH_RESULTS|

<h2 id="tocS_ProvisioningRequest">ProvisioningRequest</h2>
<!-- backwards compatibility -->
<a id="schemaprovisioningrequest"></a>
<a id="schema_ProvisioningRequest"></a>
<a id="tocSprovisioningrequest"></a>
<a id="tocsprovisioningrequest"></a>

```json
{
  "descriptorKind": "DATAPRODUCT_DESCRIPTOR",
  "descriptor": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|descriptorKind|[DescriptorKind](#schemadescriptorkind)|true|none|Values:<br> * `DATAPRODUCT_DESCRIPTOR` - Complete descriptor of a data product. It is used in the data product level provisioning workflow.<br> * `COMPONENT_DESCRIPTOR` - Provisioning descriptor for a single data product component. Includes both the complete data product descriptor (`dataProduct` object field) and the id of the component to be provisioned (`componentIdToProvision` string field).<br> * `DATAPRODUCT_DESCRIPTOR_WITH_RESULTS` - This value is not currently used in the scope of a specific provisioner.|
|descriptor|string|true|none|Descriptor specification in yaml format. Its structure changes according to `descriptorKind`.|

<h2 id="tocS_ProvisioningStatus">ProvisioningStatus</h2>
<!-- backwards compatibility -->
<a id="schemaprovisioningstatus"></a>
<a id="schema_ProvisioningStatus"></a>
<a id="tocSprovisioningstatus"></a>
<a id="tocsprovisioningstatus"></a>

```json
{
  "status": "RUNNING",
  "result": "string",
  "info": {
    "publicInfo": {},
    "privateInfo": {}
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|status|string|true|none|none|
|result|string|true|none|none|
|info|[Info](#schemainfo)|false|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|status|RUNNING|
|status|COMPLETED|
|status|FAILED|

<h2 id="tocS_ValidationResult">ValidationResult</h2>
<!-- backwards compatibility -->
<a id="schemavalidationresult"></a>
<a id="schema_ValidationResult"></a>
<a id="tocSvalidationresult"></a>
<a id="tocsvalidationresult"></a>

```json
{
  "valid": true,
  "error": {
    "errors": [
      "string"
    ]
  }
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|valid|boolean|true|none|none|
|error|[ValidationError](#schemavalidationerror)|false|none|none|

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "errors": [
    "string"
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|errors|[string]|true|none|none|

<h2 id="tocS_ProvisionInfo">ProvisionInfo</h2>
<!-- backwards compatibility -->
<a id="schemaprovisioninfo"></a>
<a id="schema_ProvisionInfo"></a>
<a id="tocSprovisioninfo"></a>
<a id="tocsprovisioninfo"></a>

```json
{
  "request": "string",
  "result": "string"
}

```

Information related to the provisioning workflow of a data product component

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|request|string|true|none|Provisioning descriptor of type `COMPONENT_DESCRIPTOR` (see [DescriptorKind](#/components/schemas/DescriptorKind) schema) in JSON format. It had been used to provision the data product component|
|result|string|true|none|Result message (e.g. a provisiong error or a success message returned by the specific provisioner in the [ProvisioningStatus](#/components/schemas/ProvisioningStatus))|

<h2 id="tocS_SystemError">SystemError</h2>
<!-- backwards compatibility -->
<a id="schemasystemerror"></a>
<a id="schema_SystemError"></a>
<a id="tocSsystemerror"></a>
<a id="tocssystemerror"></a>

```json
{
  "error": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|error|string|true|none|none|

<h2 id="tocS_Info">Info</h2>
<!-- backwards compatibility -->
<a id="schemainfo"></a>
<a id="schema_Info"></a>
<a id="tocSinfo"></a>
<a id="tocsinfo"></a>

```json
{
  "publicInfo": {},
  "privateInfo": {}
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|publicInfo|object|true|none|Fields to display in the Marketplace UI. Note that only the values compliant to specific structures will be rendered in the "Technical Information" card of the Marketplace pages. [Check the documentation](https://docs.internal.witboost.agilelab.it/docs/p3_tech/p3_customizations/p3_4_templates/infrastructureTemplate#specific-provisioner-api-details) for additional details|
|privateInfo|object|true|none|All the values in this object will be stored in the deployed descriptor, but will not be shown in the Marketplace UI|
