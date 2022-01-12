# flows

Prefect multi-module flow running on Kubernetes.

## Getting started

Prerequisites:

- docker compose
- [k3d](https://github.com/rancher/k3d) to create a k3s kubes cluster
- python 3

Install virtualenv:

```
make install
```

Create the kubes cluster:

```
make cluster
```

Install the kubes prefect agent (set your kube context before running this):

```
make install-kube-agent
```

## Usage

Get started:

```
make install
```

Set your API key:

```
 export PREFECT__CLOUD__API_KEY=....
```

Create the project (required only once):

```
prefect create project example --skip-if-exists
```

Build and push the docker image:

```
make publish
```

Run the flow in the local venv:

```
make prefect-run-local
```

Register the flow:

```
make prefect-register
```

You can now run the registered flow. When running the registered flow, a flow run will be created on Prefect Cloud which captures the status and logs.

Run the registered flow locally in docker without an agent:

```
make prefect-run-agentless
```

Trigger the registered flow to run on kubes via the agent:

```
make prefect-run
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
