# flows

Prefect multi-module flows running on Kubernetes.

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

Run the hello flow in the local venv:

```
make run-hello-local
```

Register the flows:

```
make register
```

You can now run the registered flows. When running the registered flows, a flow run will be created on Prefect Cloud which captures the status and logs.

Run the registered hello flow locally in docker without an agent:

```
make run-hello-agentless
```

Trigger the registered hello flow to run on kubes via the agent:

```
make run-hello-kubes
```

Trigger the registered dask flow to run on kubes via the agent:

```
make run-dask-kubes
```

Show pods other than the prefect agent:

```
kubectl get pod -l app!=prefect-agent
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
