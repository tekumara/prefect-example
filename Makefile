## install kubes agent
prefect-k8s-install: $(venv)
	prefect agent kubernetes install -k "$$PREFECT__CLOUD__API_KEY" --rbac --label kube | kubectl apply -f -

## register flow
prefect-register: $(venv)
	$(venv)/bin/prefect register --project example -m flows.example

## run flow on kubes
prefect-run: $(venv)
	$(venv)/bin/prefect run -n "hello-flow" --watch

## run flow locally
prefect-run-local: $(venv)
	$(venv)/bin/prefect run -m flows.example

include *.mk
