## create k3s cluster
cluster:
	k3d cluster create prefect --registry-create prefect-registry:0.0.0.0:5000 --wait

## install kubes agent
prefect-k8s-install: $(venv)
	prefect agent kubernetes install -k "$(PREFECT__CLOUD__API_KEY)" --rbac --label kube | kubectl apply -f -

## build docker image
build:
	docker compose build app

## push docker image to registry
push:
	docker compose push app

## build and push docker image
publish: build push

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
