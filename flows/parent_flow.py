from prefect import Flow
from prefect.run_configs import KubernetesRun
from prefect.storage.module import Module
from prefect.tasks.prefect import create_flow_run, wait_for_flow_run

with Flow(
    "parent",
    storage=Module(__name__),
    run_config=KubernetesRun(
        image="prefect-registry:5555/prefect-example:v1",
        labels=["kube"],
        cpu_limit=1,
        cpu_request=1,
        memory_limit="1Gi",
        # needed to get pull latest version of a mutated image tag
        image_pull_policy="Always",
    ),
) as flow:
    run_child = create_flow_run(flow_name="child", project_name="example")
    # run_child.result = LocalResult(dir='/tmp/results')
    wait_for_child = wait_for_flow_run(run_child, raise_final_state=True)
    # wait_for_child.max_retries = 3
    # wait_for_child.retry_delay=timedelta(seconds=10)

if __name__ == "__main__":
    flow.run()
