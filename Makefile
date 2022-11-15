## create k3s cluster
cluster:
	k3d cluster create prefect --registry-create prefect-registry:0.0.0.0:5555 --wait
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write prefect)"

## install prefect agent into kubes cluster
install-kube-agent: $(venv)
	prefect agent kubernetes install -k "$(PREFECT__CLOUD__API_KEY)" --rbac --label kube | kubectl apply -f -
	kubectl apply -f infra/dask-kubernetes-rbac.yaml

## build docker image
build:
	docker compose build app

## push docker image to registry
push:
	docker compose push app

## build and push docker image
publish: build push

## register flows
register: $(venv)
	$(venv)/bin/prefect register --project example -m flows.hello_flow -m flows.dask_flow -m flows.parent_flow -m flows.child_flow -m flows.loggers

## run hello-flow in local venv
run-hello-local: $(venv)
	$(venv)/bin/prefect run -m flows.hello_flow

## run registered hello-flow on kubes via agent
run-hello-kubes: $(venv)
	$(venv)/bin/prefect run -n "hello-flow" --watch

## run registered hello-flow locally in docker
run-hello-agentless:
	docker compose run app prefect run -n hello-flow --execute

## run registered loggers-flow locally in docker
run-loggers-agentless:
	docker compose run app prefect run -n loggers-flow --execute

## run registered dask flow on kubes via agent
run-dask-kubes: $(venv)
	$(venv)/bin/prefect run -n "Dask Kubernetes Flow" --watch

## run registered parent flow on kubes via agent
run-parent: $(venv)
	$(venv)/bin/prefect run -n "parent" --watch

include *.mk
