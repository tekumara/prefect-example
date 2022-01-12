## create k3s cluster
cluster:
	k3d cluster create prefect --registry-create prefect-registry:0.0.0.0:5000 --wait
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write prefect)"

## install prefect agent into kubes cluster
install-kube-agent: $(venv)
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

## run flow in local venv
prefect-run-local: $(venv)
	$(venv)/bin/prefect run -m flows.example

## run registered flow on kubes via agent
prefect-run-kubes: $(venv)
	$(venv)/bin/prefect run -n "hello-flow" --watch

## run registered flow locally in docker
prefect-run-agentless:
	docker compose run app

include *.mk
