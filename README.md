# flows

Prefect multi-module flows running on Kubernetes:

- [hello-flow](flows/hello_flow.py) a basic hello world flow
- [Dask Kubernetes Flow](flows/dask_flow.py) a flow that uses an ephemeral Dask cluster on Kubernetes
- see [flows/](flows/) for more!

## Getting started

Prerequisites:

- docker compose
- [k3d](https://github.com/rancher/k3d) to create a k3s kubes cluster
- python 3

To start:

- Install virtualenv: `make install`
- Create the kubes cluster: `make cluster`
- Set your kube context
- Install the kubes perfect agent: `make install-kube-agent`

## Usage

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
