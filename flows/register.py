from prefect.storage.module import Module
from flows.example import flow
from prefect.run_configs import KubernetesRun
from prefect.storage import Local

# storage = Local(
#     path=f"/opt/prefect/flows/{FLOW_NAME}.py",
#     stored_as_script=True,
#     add_default_labels=False,
# )

flow.storage = Module("flows.example")

flow.run_config = KubernetesRun(
    # env={"PREFECT__LOGGING__LEVEL": "INFO",
    #         "PYTHONPATH": "${PYTHONPATH}:/workdir/"},
    image="prefect-example:v1",
    labels=['kube'],
    # cpu_limit=1,
    # cpu_request=1,
    # memory_limit="1Gi"
)

flow.register(project_name="example")
