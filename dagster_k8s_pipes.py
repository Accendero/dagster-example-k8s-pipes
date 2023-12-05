# dagster_k8s_pipes.py

from dagster import op, OpExecutionContext, Definitions, job
from dagster_k8s import PipesK8sClient


@op
def k8s_pipes_op(context: OpExecutionContext, k8s_pipes_client: PipesK8sClient):
    result = k8s_pipes_client.run(
        context=context,
        image="pipes-example:v1",
        env={
            "AWS_BUCKET": "dagster",
            "AWS_ACCESS_KEY_ID": "minio",
            "AWS_SECRET_ACCESS_KEY": "minio123",
            "AWS_ENDPOINT_URL": "http://host.minikube.internal:9000",
        },
        command=[
            "python", "containerized_script.py", "--obj", "example-run-id/test-file.txt",
        ]
    ).get_materialize_result()
    context.log.info(f"Read in {result.metadata['key'].text} from S3, from bucket {result.metadata['bucket'].text}")
    context.log.info(f"Processed {result.metadata['key'].text} and wrote to {result.metadata['processed_key'].text}")


@job
def k8s_pipes_job():
    k8s_pipes_op()


defs = Definitions(
    jobs=[k8s_pipes_job],
    resources={
        "k8s_pipes_client": PipesK8sClient(),
    },
)
