# flows

Prefect examples

## Usage

Set your API key:

```
 export PREFECT__CLOUD__API_KEY=....
```

Create the project (required only once):

```
prefect create project example --skip-if-exists
```

Install the kube prefect agent:

```
make prefect-k8s-install
```

Register the flow:

```
make prefect-register
```
