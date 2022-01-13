# see https://medium.com/slateco-blog/prefect-x-kubernetes-x-ephemeral-dask-power-without-responsibility-6e10b4f2fe40

from dask_kubernetes import KubeCluster, make_pod_spec
from prefect.storage import Docker
from prefect import task, Flow
from prefect.executors import DaskExecutor

# Configure a storage object, by default prefect's latest image will be used
storage = Docker(
    base_image="prefecthq/prefect:0.15.1-python3.7",
    python_dependencies=[
        "dask-kubernetes==2021.3.1",
    ],
    registry_url="YOUR_COOL_REPO",
    extra_dockerfile_commands=[
        "RUN apt-get update && apt-get install -y curl &&\
        curl -LO https://dl.k8s.io/release/v1.21.2/bin/linux/amd64/kubectl &&\
        install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl &&\
        rm -rf /var/lib/apt/lists/*",
    ],
)

# Define some tasks for us to run in our flow
@task
def extract() -> list:
    return [1, 2, 3, 4, 5, 6]


@task(max_retries=3, retry_delay=timedelta(seconds=15))
def transform(number: int)->int:
    return number * 2


@task()
def load(numbers:list)->list:
    return [i for i in numbers if i]

with Flow(
    "Dask Kubernetes Flow",
    storage=storage,
    executor=DaskExecutor(
        cluster_class=lambda: KubeCluster(make_pod_spec(image=prefect.context.image)),
        adapt_kwargs={"minimum": 2, "maximum": 3},
    ),
    run_config=KubernetesRun(),
) as flow:
    numbers = extract()

    numbers = extract()
    tranformed_numbers = transform.map(numbers)
    numbers_twice = transform.map(tranformed_numbers)
    result = load(numbers=numbers_twice)
