from prefect import Flow
from prefect.tasks.prefect import create_flow_run, wait_for_flow_run

with Flow("parent") as flow:
    run_child = create_flow_run(flow_name="child", project_name="example")
    wait_for_child = wait_for_flow_run(run_child, raise_final_state=True)


flow.run()
