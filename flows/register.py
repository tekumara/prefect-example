from prefect.run_configs import KubernetesRun
from prefect.storage.module import Module

import flows.example
from flows.example import flow

flow.storage = Module(flows.example.__name__)

flow.run_config = KubernetesRun(
    image="prefect-example:v1", labels=["kube"], cpu_limit=1, cpu_request=1, memory_limit="1Gi"
)

flow.register(project_name="example")
