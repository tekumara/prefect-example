# flows

Prefect multi-module flow running on Kubernetes.

## Getting started

Prerequisites:

- [k3d](https://github.com/rancher/k3d) to create a kubes cluster
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
make prefect-k8s-install
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

Register the flow:

```
make prefect-register
```

Run the flow on kubes:

```
make prefect-run
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
