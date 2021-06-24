# Solace config management from Azure DevOps Pipeline

## About

This repository has config and scripts required to create sample Azure DevOps flows. These flows demostrate a simple Solace config management from Azure DevOps CI/CD pipeline.

### Solace DevOps Pipeline

![Solace DevOps Pipeline](img/Picture1.png?raw=true "Solace DevOps Pipeline")

## Pre-Requisites

- [GitHub](http://www.github.com) account
- [Microsoft DevOps](http://dev.azure.com) account
- [Visual Studio Code](http://code.visualstudio.com) (Optional)
- [Variable Groups](https://medium.com/slalom-technology/learn-to-use-variable-groups-in-azure-devops-pipelines-203a485b4731) by ServiceName
  - HOST (Solace Management URL. eg: http://my-solace-instance.messaging.solace.cloud:943)
  - SEMPUSER (SEMP CLI user: eg: my-solace-instance-admin)
  - SEMPPASS (SEMP User password)
  - VPN (MessageVPN Name. eg:my-solace-instance) (Optional)

  __Variable groups not required for Ansible playbook based pipeline__

## Sample Pipelines

### [Inline](create-queue.yml)

This pipeline has all required varaibles inside the pipeline YAML itslef. This creates a single queue and all queue properties are hardcoded into the YAML itself. There is no external dependency to this flow.

### [Python](azure-poc2-queues2.yml)

This pipeline triggers an external python script [provision-queue.py](scripts/provision-queue.py) that reads all variable information (such as Queue name, owner, spool size) are read in from an YAML file [queues.yaml](input/queues.yaml).

This pipeline also uses template json to generate the payload. This should make this pipeline extensible for other artifacts such as client-username, RDP, etc.

This pipeline also uses template json to generate the payload. This should make this pipeline extensible for other artifacts such as client-username, RDP, etc.

### [Ansible](azure-poc-ansible.yml)

This pipeline triggers an Ansible playbook for queue creation using a [template playbook](ansible-create-queues.yml) with an [inventory file](ansible-aws-brokers.ini).

This can be extended for other VPN objects as well.

## Authors

Ramesh Natarajan (nram) (ramesh.natarajan@solace.com), Solace PSG