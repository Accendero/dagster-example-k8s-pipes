# dagster-k8s-pipes

This example illustrates how to use Dagster to launch a containerized script using the `dagster_k8s.k8s_pipes_client`.

## How it works

The dagster job uses the `k8s_pipes_client` to issue a dynamic command to the container it runs. The container
in this example will fetch a file from s3-like storage, and then write it to another location. Once complete,
the container uses the pipes context to send metadata back to the dagster job.

## Setup

* Install [poetry](https://python-poetry.org/docs/#installation)
* Install [docker](https://docs.docker.com/get-docker/)
* Install [minikube](https://minikube.sigs.k8s.io/docs/start/)
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## Running the example

To run this example, you will need to have access to a kubernetes cluster. This example has been tested with
minikube.

1. Install requirements

    ```bash
    poetry install
    ```

1. Start minikube

    ```bash
    minikube start
    ```

1. Build the docker image using minikube's docker daemon

    ```bash
    eval $(minikube -p minikube docker-env)
    docker build -t pipes-example:v1 .
    ```
   Note: If you have trouble getting the correct context here, first get the default context, and then run the above
   commands.
    ```bash
   docker context use default
   ```

1. Run the dagster dev services

    ```bash
   dagster dev -f dagster_k8s_pipes.py
   ```

1. Start the support services

     ```bash
    docker compose up -d
    ```

1. Navigate to the [dagster webserver UI](http://localhost:3000) and launch a job

1. If you wish to view the jobs running in minikube, you can run the dashboard

    ```bash
    minikube dashboard
    ```
1. When you are done, you can stop the support services

    ```bash
    docker compose down
    ```
   Stop the dagster dev services with `ctrl-c` and then stop minikube with
    ```bash
    minikube stop
    ```