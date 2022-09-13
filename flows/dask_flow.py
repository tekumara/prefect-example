# adapted from https://medium.com/slateco-blog/prefect-x-kubernetes-x-ephemeral-dask-power-without-responsibility-6e10b4f2fe40
import prefect
from dask_kubernetes import KubeCluster, make_pod_spec
from prefect import Flow, task
from prefect.executors import DaskExecutor
from prefect.run_configs import KubernetesRun
from prefect.storage.module import Module


# Define some tasks for us to run in our flow
@task
def extract() -> list:
    return [1, 2, 3, 4, 5, 6]


@task
def transform(number: int) -> int:
    return number * 2


@task
def load(numbers: list) -> list:
    return [i for i in numbers if i]


image = "prefect-registry:5555/prefect-example:v1"

with Flow(
    "Dask Kubernetes Flow",
    storage=Module(__name__),
    executor=DaskExecutor(
        cluster_class=lambda: KubeCluster(make_pod_spec(image=prefect.context.image)),
        adapt_kwargs={"minimum": 2, "maximum": 3},
    ),
    run_config=KubernetesRun(labels=["kube"], image=image, image_pull_policy="Always"),
) as flow:
    numbers = extract()

    numbers = extract()
    transformed_numbers = transform.map(numbers)
    numbers_twice = transform.map(transformed_numbers)
    result = load(numbers=numbers_twice)
