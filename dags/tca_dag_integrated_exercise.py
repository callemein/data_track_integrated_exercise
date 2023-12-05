from airflow import DAG
from airflow.providers.amazon.aws.operators.batch import BatchOperator
from datetime import datetime as dt

dag = DAG(
    dag_id="tca_ingest_data_points",
    description="Ingest data_points",
    default_args={"owner": "Timothy Callemein"},
    schedule_interval="@daily",
    start_date=dt(2023, 9, 1),
)

table = "data_points"

with dag:
    ingest = BatchOperator(
        task_id="tca_dp_ingest",
        job_name="tca_dp_ingest",
        job_definition="dt_tca_ingest",
        job_queue="integrated-exercise-job-queue",
        region_name="eu-west-1",
        container_overrides={
            "environment": [
                {
                    "name": "APP_TYPE",
                    "value": 'ingest',
                },
                {
                    "name": "APP_TABLE",
                    "value": table,
                },
                {
                    "name": "APP_DATE",
                    "value": "{{ds}}",
                },
            ],
        },
    )

    transform = BatchOperator(
        task_id="tca_dp_transform",
        job_name="tca_dp_transform",
        job_definition="dt_tca_ingest",
        job_queue="integrated-exercise-job-queue",
        region_name="eu-west-1",
        container_overrides={
            "environment": [
                {
                    "name": "APP_TYPE",
                    "value": 'transform',
                },
                {
                    "name": "APP_DATE",
                    "value": "{{ds}}",
                },
            ],
        },
    )

    egress = BatchOperator(
        task_id="tca_dp_egress",
        job_name="tca_dp_egress",
        job_definition="dt_tca_ingest",
        job_queue="integrated-exercise-job-queue",
        region_name="eu-west-1",
        container_overrides={
            "environment": [
                {
                    "name": "APP_TYPE",
                    "value": 'egress',
                },
                {
                    "name": "APP_DATE",
                    "value": "{{ds}}",
                },
            ],
        },
    )

    ingest >> transform >> egress
