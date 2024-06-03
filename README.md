<p align="center">
    <a href="https://www.agilelab.it/witboost">
        <img src="docs/img/witboost_logo.svg" alt="witboost" width=600 >
    </a>
</p>

Designed by [Agile Lab](https://www.agilelab.it/), witboost is a versatile platform that addresses a wide range of sophisticated data engineering challenges. It enables businesses to discover, enhance, and productize their data, fostering the creation of automated data platforms that adhere to the highest standards of data governance. Want to know more about witboost? Check it out [here](https://www.agilelab.it/witboost) or [contact us!](https://www.agilelab.it/contacts)

This repository is part of our [Starter Kit](https://github.com/agile-lab-dev/witboost-starter-kit) meant to showcase witboost's integration capabilities and provide a "batteries-included" product.

# Python Scaffold

- [Overview](#overview)
- [Building](#building)
- [Running](#running)
- [OpenTelemetry Setup](specific-provisioner/docs/opentelemetry.md)
- [Deploying](#deploying)
- [API specification](docs/API.md)

## Overview

This project provides a scaffold to develop a Specific Provisioner from scratch using Python & FastAPI.

### What's a Specific Provisioner?

A Specific Provisioner is a microservice which is in charge of deploying components that use a specific technology. When the deployment of a Data Product is triggered, the platform generates it descriptor and orchestrates the deployment of every component contained in the Data Product. For every such component the platform knows which Specific Provisioner is responsible for its deployment, and can thus send a provisioning request with the descriptor to it so that the Specific Provisioner can perform whatever operation is required to fulfill this request and report back the outcome to the platform.

You can learn more about how the Specific Provisioners fit in the broader picture [here](https://docs.witboost.agilelab.it/docs/p2_arch/p1_intro/#deploy-flow).

### Software stack

This microservice is written in Python 3.11, using FastAPI for the HTTP layer. Project is built with Poetry and supports packaging as Wheel and Docker image, ideal for Kubernetes deployments (which is the preferred option).

## Building

**Requirements:**

- Python 3.11
- Poetry

**Installing**:

To set up a Python environment we use [Poetry](https://python-poetry.org/docs/):

```
curl -sSL https://install.python-poetry.org | python3 -
```

Once Poetry is installed and in your `$PATH`, you can execute the following:

```
poetry --version
```

If you see something like `Poetry (version x.x.x)`, your install is ready to use!

Install the dependencies defined in `specific-provisioner/pyproject.toml`:
```
cd specific-provisioner
poetry install
```

*Note:* All the following commands are to be run in the Poetry project directory with the virtualenv enabled.

**Type check:** is handled by mypy:

```bash
poetry run mypy src/
```

**Tests:** are handled by pytest:

```bash
poetry run pytest --cov=src/ tests/. --cov-report=xml
```

**Artifacts & Docker image:** the project leverages Poetry for packaging. Build package with:

```
poetry build
```

The Docker image can be built with:

```
docker build .
```

More details can be found [here](specific-provisioner/docs/docker.md).

*Note:* the version for the project is automatically computed using information gathered from Git, using branch name and tags. Unless you are on a release branch `1.2.x` or a tag `v1.2.3` it will end up being `0.0.0`. You can follow this branch/tag convention or update the version computation to match your preferred strategy.

**CI/CD:** the pipeline is based on GitLab CI as that's what we use internally. It's configured by the `.gitlab-ci.yaml` file in the root of the repository. You can use that as a starting point for your customizations.

## Running

To run the server locally, use:

```bash
cd specific-provisioner
source $(poetry env info --path)/bin/activate # only needed if venv is not already enabled
uvicorn src.main:app --host 127.0.0.1 --port 8091
```

By default, the server binds to port 8091 on localhost. After it's up and running you can make provisioning requests to this address. You can also check the API documentation served [here](http://127.0.0.1:8091/docs).


## Descriptor

Create deployment descriptor, copy the descriptor from witboost UI.
Then use a YAML stringify ( jsonformatter.org ) and put into the {"HI"} placeholder.

Example:

```
Body request
{
    "descriptor": {"Hi"},
    "descriptorKind": "DATAPRODUCT_DESCRIPTOR",
    "removeData": false
}

//YAML

dataproduct:
		<descriptor, indented one level>
componentIdToProvision: <id>   //urn:dmb:cmp:distribution:network-status:0:confluent-kafka-streams-ingestion


//REAL DESCRIPTOR

dataProductOwnerDisplayName: Paolo Platter
environment: production
domain: distribution
kind: dataproduct
domainId: urn:dmb:dmn:distribution
id: urn:dmb:dp:distribution:network-status:0
description: Network Status that provides better insights to CS Agents
devGroup: datameshplatform
ownerGroup: paolo.platter_agilelab.it
dataProductOwner: user:paolo.platter_agilelab.it
email: distribution@agilelab.it
version: 0.1.0-SNAPSHOT-12
name: Network Status
fullyQualifiedName: Network Status
maturity: null
useCaseTemplateId: urn:dmb:utm:analytics-data-product-template:0.0.0
infrastructureTemplateId: urn:dmb:itm:aws-cdp-outputport-mock-provisioner:1
billing: {}
tags:
  - tagFQN: GDPR
    source: Tag
    labelType: Manual
    state: Confirmed
specific: {}
components:
  - kind: workload
    id: urn:dmb:cmp:distribution:network-status:0:confluent-kafka-streams-ingestion
    description: Confluent Kafka Streams Ingestion
    name: Confluent Kafka Streams Ingestion
    fullyQualifiedName: Confluent Kafka Streams Ingestion
    version: 0.0.0
    infrastructureTemplateId: urn:dmb:itm:aws-cdp-outputport-mock-provisioner:1
    useCaseTemplateId: urn:dmb:utm:confluent-kafka-streams-workload-template.1
    dependsOn: []
    platform: Confluent
    technology: Kafka Streams
    workloadType: batch
    connectionType: DataPipeline
    tags: []
    readsFrom: []
    specific:
      cluster: confluent-cluster
      applicationId: network-status-kstreams-01
      mainClass: io.confluent.developer.KafkaStreamsApplication
      stateDir: /${java.io.tmpdir}/kafka-streams
      acceptableRecoveryLag: 10000
      cacheMaxBytesBuffering: 10485760
      clientId: null
      defaultDeserializationExceptionHandler: default.deserialization.exception.handler
      defaultProductionExceptionHandler: default.production.exception.handler
      defaultWindowedKeySerdeInner: Serdes.ByteArray().getClass().getName()
      defaultWindowedValueSerdeInner: Serdes.ByteArray().getClass().getName()
      maxTaskIdleMs: 0
      maxWarmupReplicas: 2
      numStreamThreads: 1
      retries: 2
      retryBackoffMs: 100
      statestoreCacheMaxBytes: 10485760
  - kind: workload
    id: urn:dmb:cmp:distribution:network-status:0:databricks-workload
    description: Databricks Workload
    name: Databricks Workload
    fullyQualifiedName: Databricks Workload
    version: 0.0.0
    infrastructureTemplateId: urn:dmb:itm:aws-cdp-outputport-mock-provisioner:1
    useCaseTemplateId: urn:dmb:utm:databricks-workload-template.1
    dependsOn: []
    platform: Databricks
    technology: spark
    workloadType: batch
    connectionType: DataPipeline
    tags: []
    readsFrom: []
    specific:
      cluster: databricks-cluster
      jobName: network-status-databricks-01
      notebook: ./notebook/main.py
      jobConfig:
        args: []
        dependencies: []
        driverCores: 2
        driverMemory: 2g
        executorCores: 2
        executorMemory: 2g
        numExecutors: 3
        logLevel: INFO
        conf: {}
        schedule:
          cronExpression: 0 0 0 * *
          startDate: 2024-03-06T19:08:00Z
          endDate: 2025-10-06T18:08:00Z
  - kind: storage
    id: urn:dmb:cmp:distribution:network-status:0:input-kafka-topic
    description: This is the Kafka Topic used for data ingestion
    name: Input Kafka Topic
    fullyQualifiedName: null
    version: 0.0.0
    infrastructureTemplateId: urn:dmb:itm:aws-cdp-outputport-mock-provisioner:1
    useCaseTemplateId: urn:dmb:utm:confluent-kafka-topic-storage-template.1
    platform: Confluent
    technology: Kafka
    creationDate: null
    startDate: null
    processDescription: null
    dependsOn: []
    tags: []
    specific:
      topicName: network-status-realtime-topic
      partitions: "3"
      cluster: confluent-cluster
      compressionType: producer
      confluentKeySchemaValidation: "false"
      confluentKeySubjectNameStrategy: io.confluent.kafka.serializers.subject.TopicNameStrategy
      confluentTierEnable: "false"
      confluentTierLocalHotsetBytes: "-1"
      confluentTierLocalHotsetMs: "86400000"
      confluentValueSchemaValidation: "false"
      confluentValueSubjectNameStrategy: io.confluent.kafka.serializers.subject.TopicNameStrategy
      deleteRetentionMs: "86400000"
      fileDeleteDelayMs: "60000"
      flushMessages: "9223372036854776000"
      flushMs: "9223372036854776000"
      followerReplicationThrottledReplicas: ""
      indexIntervalBytes: "4096"
      leaderReplicationThrottledReplicas: ""
      localRetentionBytes: "-2"
      localRetentionMs: "-2"
      maxCompactionLagMs: "9223372036854776000"
      maxMessageBytes: "1048588"
      messageFormatVersion: 3.0-IV1
      messageTimestampAfterMaxMs: "9223372036854776000"
      messageTimestampBeforeMaxMs: "9223372036854776000"
      messageTimestampDifferenceMaxMs: "9223372036854776000"
      messageTimestampType: CreateTime
      minCleanableDirtyRatio: "0.5"
      minCompactionLagMs: "0"
      minInsyncReplicas: "1"
      preallocate: "false"
      remoteStorageEnable: "false"
      retentionBytes: "-1"
      retentionMs: "604800000"
      segmentBytes: "1073741824"
      segmentIndexBytes: "10485760"
      segmentJitterMs: "0"
      segmentMs: "604800000"
      uncleanLeaderElectionEnable: "false"
      confluentClusterLinkAllowLegacyMessageFormat: "false"
      confluentPlacementConstraints: "{}"
      messageDownconversionEnable: "true"
      replicationFactor: "3"
  - kind: outputport
    id: urn:dmb:cmp:distribution:network-status:0:snowflake-output-port
    description: Network Status table
    name: Snowflake Output Port
    fullyQualifiedName: Snowflake Output Port
    version: 0.0.0
    infrastructureTemplateId: urn:dmb:itm:snowflake-outputport-provisioner:0
    useCaseTemplateId: urn:dmb:utm:snowflake-outputport-template:0.0.0
    dependsOn:
      - urn:dmb:cmp:distribution:network-status:0:snowflake-storage-area
    platform: Snowflake
    technology: Snowflake
    outputPortType: SQL
    creationDate: 2024-03-06T16:00:19.621Z
    startDate: 2024-03-06T16:00:19.621Z
    dataContract:
      schema:
        - name: ID
          description: A unique identifier for each record test
          dataType: NUMBER
          precision: 38
          scale: 0
          tags: []
        - name: Timestamp
          description: The date and time when the status was recorded.
          dataType: DATE
          tags: []
        - name: NetworkID
          description: A unique identifier for each network segment or component. This
            could reference a cell site, a region, or any specific part of the
            network infrastructure
          dataType: TEXT
          dataLength: 16777216
          tags:
            - tagFQN: Network Identifier
              source: Glossary
              labelType: Manual
              state: Confirmed
        - name: Status
          description: The current status of the network segment (e.g., "Operational",
            "Degraded", "Down")
          dataType: TEXT
          dataLength: 16777216
          tags:
            - tagFQN: Network Status
              source: Glossary
              labelType: Manual
              state: Confirmed
        - name: SignalStrength
          description: Measures the strength of the signal in a specific unit (e.g., dBm).
            This could vary depending on the network type (e.g., 4G, 5G)
          dataType: NUMBER
          precision: 38
          scale: 0
          tags: []
        - name: Latency
          description: The delay (typically measured in milliseconds) experienced in the
            network
          dataType: NUMBER
          precision: 38
          scale: 0
          tags: []
        - name: TrafficVolume
          description: The amount of data being transmitted through the network segment in
            a specific unit (e.g., Megabytes, Gigabytes) over a certain period
          dataType: NUMBER
          precision: 38
          scale: 0
          tags:
            - tagFQN: Roaming
              source: Glossary
              labelType: Manual
              state: Confirmed
            - tagFQN: ARPU
              source: Glossary
              labelType: Manual
              state: Confirmed
        - name: ErrorRate
          description: The rate of errors encountered in the network traffic (e.g., packet
            loss percentage)
          dataType: NUMBER
          precision: 38
          scale: 0
          tags:
            - tagFQN: QoS
              source: Glossary
              labelType: Manual
              state: Confirmed
        - name: Capacity
          description: The maximum amount of traffic the network segment can handle, often
            measured in terms of concurrent connections or data throughput
            capacity (e.g., Gbps)
          dataType: NUMBER
          precision: 38
          scale: 0
          tags:
            - tagFQN: Network Capacity
              source: Glossary
              labelType: Manual
              state: Confirmed
        - name: Utilization
          description: The percentage of the network capacity that is currently being used
          dataType: NUMBER
          precision: 38
          scale: 0
          tags:
            - tagFQN: PII
              source: Tag
              labelType: Manual
              state: Confirmed
        - name: LastMaintenance
          description: The date and time of the last maintenance activity conducted on the
            network segment
          dataType: DATE
          tags:
            - tagFQN: PII
              source: Tag
              labelType: Manual
              state: Confirmed
        - name: Notes
          description: Any additional notes or comments about the network status,
            maintenance activities, or observed issues
          dataType: TEXT
          dataLength: 16777216
          tags: []
      termsAndConditions: Can be used for production purposes.
      SLA:
        intervalOfChange: 2BD
        timeliness: 2BD
        upTime: 99.9%
    tags: []
    sampleData: {}
    semanticLinking: []
    specific:
      viewName: NETWORK_STATUS_VIEW
      tableName: NETWORK_STATUS
      database: DISTRIBUTION
      schema: NETWORKSTATUS_0
    dataSharingAgreement:
      purpose: Foundational data for downstream sue cases.
      billing: None.
      security: Platform standard security policies.
      intendedUsage: Any downstream use cases.
      limitations: Needs joining with other datasets (eg customer data) for most
        analytical use cases.
      lifeCycle: Data loaded every two days and typically never deleted.
      confidentiality: None.
  - kind: storage
    id: urn:dmb:cmp:distribution:network-status:0:snowflake-storage-area
    description: Internal storage area for snowflake data
    name: Snowflake Storage Area
    fullyQualifiedName: Snowflake Storage Area
    version: 0.0.0
    infrastructureTemplateId: urn:dmb:itm:snowflake-storage-provisioner:0
    useCaseTemplateId: urn:dmb:utm:snowflake-storage-template:0.0.0
    dependsOn: []
    platform: Snowflake
    technology: Snowflake
    StorageType: Database
    tags: []
    specific:
      database: DISTRIBUTION
      schema: NETWORKSTATUS_0
      tables:
        - tableName: NETWORK_STATUS
          schema:
            - name: ID
              description: A unique identifier for each record
              dataType: NUMBER
              precision: 38
              scale: 0
              tags: []
            - name: Timestamp
              description: The date and time when the status was recorded.
              dataType: DATE
              tags: []
            - name: NetworkID
              description: A unique identifier for each network segment or component. This
                could reference a cell site, a region, or any specific part of
                the network infrastructure
              dataType: TEXT
              dataLength: 16777216
              tags: []
            - name: Status
              description: The current status of the network segment (e.g., "Operational",
                "Degraded", "Down")
              dataType: TEXT
              dataLength: 16777216
              tags: []
            - name: SignalStrength
              description: Measures the strength of the signal in a specific unit (e.g., dBm).
                This could vary depending on the network type (e.g., 4G, 5G)
              dataType: NUMBER
              precision: 38
              scale: 0
              tags: []
            - name: Latency
              description: The delay (typically measured in milliseconds) experienced in the
                network
              dataType: NUMBER
              precision: 38
              scale: 0
              tags: []
            - name: TrafficVolume
              description: The amount of data being transmitted through the network segment in
                a specific unit (e.g., Megabytes, Gigabytes) over a certain
                period
              dataType: NUMBER
              precision: 38
              scale: 0
              tags: []
            - name: ErrorRate
              description: The rate of errors encountered in the network traffic (e.g., packet
                loss percentage)
              dataType: NUMBER
              precision: 38
              scale: 0
              tags: []
            - name: Capacity
              description: The maximum amount of traffic the network segment can handle, often
                measured in terms of concurrent connections or data throughput
                capacity (e.g., Gbps)
              dataType: NUMBER
              precision: 38
              scale: 0
              tags: []
            - name: Utilization
              description: The percentage of the network capacity that is currently being used
              dataType: NUMBER
              precision: 38
              scale: 0
              tags: []
            - name: LastMaintenance
              description: The date and time of the last maintenance activity conducted on the
                network segment
              dataType: DATE
              tags: []
            - name: Notes
              description: Any additional notes or comments about the network status,
                maintenance activities, or observed issues
              dataType: TEXT
              dataLength: 16777216
              tags: []
```




## Deploying

This microservice is meant to be deployed to a Kubernetes cluster with the included Helm chart and the scripts that can be found in the `helm` subdirectory. You can find more details [here](helm/README.md).

## License

This project is available under the [Apache License, Version 2.0](https://opensource.org/licenses/Apache-2.0); see [LICENSE](LICENSE) for full details.

## About us

<p align="center">
    <a href="https://www.agilelab.it">
        <img src="docs/img/agilelab_logo.jpg" alt="Agile Lab" width=600>
    </a>
</p>

Agile Lab creates value for its Clients in data-intensive environments through customizable solutions to establish performance driven processes, sustainable architectures, and automated platforms driven by data governance best practices.

Since 2014 we have implemented 100+ successful Elite Data Engineering initiatives and used that experience to create Witboost: a technology agnostic, modular platform, that empowers modern enterprises to discover, elevate and productize their data both in traditional environments and on fully compliant Data mesh architectures.

[Contact us](https://www.agilelab.it/contacts) or follow us on:
- [LinkedIn](https://www.linkedin.com/company/agile-lab/)
- [Instagram](https://www.instagram.com/agilelab_official/)
- [YouTube](https://www.youtube.com/channel/UCTWdhr7_4JmZIpZFhMdLzAA)
- [Twitter](https://twitter.com/agile__lab)
