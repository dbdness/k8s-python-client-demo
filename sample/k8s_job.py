"""On-demand Kubernetes Job creation

This script handles Job resources within the default Kubernetes cluster context.
The following Job actions are supported:
* Create Job with single Pod
* Delete Job

This script also requires that `kubernetes` is installed within the Python
environment you are running this script in.

Variables:
    job_name (str): The desired Job name
    replicas (int): Number of replicas
    pod_labels (dict{str:str}): Labels to assign to the Pod
    container_name (str): The desired name of the container
    container_image (str): The full path to the desired container image. Repository has to be included.
    container_port (int): The exposed port from within the Job.

Functions:
    create_job() - creates and launches a Kubernetes Job based on the specified variables.
    delete_job() - deletes a Kubernetes Job with the name defined in the job_name variable.
"""

import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException


# Variables to define the K8s Job
job_name = "demo"
replicas = 1
pod_labels = {"app": "sentence-reverser"}
container_name = "sentence-reverser"
container_image = "registry.hub.docker.com/kimsen1992/sentence-reverser"
container_env_vars = [
    client.V1EnvVar(name="SENTENCE", value="Demo"),
    client.V1EnvVar(name="WEBHOOKURL",
                    value="https://webhook.site/7a3a5242-2cee-4623-8dd2-89aa8a7fdd1b")
]
container_port = 80


def main():
    # Loading default config
    config.load_kube_config()
    api_instance = client.BatchV1Api()

    # If no arguments are passed (eg. the script is run from an IDE), just create a K8s Job.
    try:
        arg = sys.argv[1]
    except IndexError:
        create_job(api_instance)
        return

    if arg == "--create":
        create_job(api_instance)
    elif arg == "--delete":
        delete_job(api_instance)
    elif arg == "--status":
        get_job_status(api_instance)
    else:
        print("Usage:\n"
              "--create\n"
              "    create K8s Job based on script variables.\n"
              "--delete\n"
              "    delete K8s Job based on script job_name variable, if Job exists.\n"
              "--status\n"
              "    get status on K8s Job based on script job_name variable, if Job exists.")


def create_job(api_instance):
    # Creating and defining Job object
    job = client.V1Job()
    job.api_version = "batch/v1"
    job.kind = "Job"
    job.metadata = client.V1ObjectMeta(name=job_name)

    # Defining Job spec with Pods
    spec = client.V1JobSpec(template=client.V1PodTemplateSpec())
    # Deleting the Job 10s after it has finished *if* supported by the server.
    spec.ttl_seconds_after_finished = 10
    spec.template.metadata = client.V1ObjectMeta(labels=pod_labels)
    job.spec = spec

    # Defining Pod container specs
    container = client.V1Container(name=container_name)
    container.image = container_image
    container.env = container_env_vars
    container.ports = [client.V1ContainerPort(container_port=container_port)]

    # restart_policy options: "Always", "OnFailure", "Never"
    spec.template.spec = client.V1PodSpec(containers=[container], restart_policy="OnFailure")

    # Creating Job
    try:
        print("Creating Job '{0}'".format(job_name))
        api_instance.create_namespaced_job(namespace="default", body=job)
        print("Success!")
    except ApiException as e:
        print("Exception thrown when creating Job: {0}".format(e))


def delete_job(api_instance):
    body = client.V1DeleteOptions()
    try:
        print("Deleting Job '{0}'".format(job_name))
        api_instance.delete_namespaced_job(namespace="default", name=job_name, body=body)
        print("Success!")
    except ApiException as e:
        print("Exception thrown when deleting Job: {0}".format(e))


def get_job_status(api_instance):
    try:
        print("Getting status for Job '{0}'".format(job_name))
        job = api_instance.read_namespaced_job(namespace="default", name=job_name)
        print(job.status)
    except ApiException as e:
        print("Exception thrown when deleting Job: {0}".format(e))


if __name__ == '__main__':
    main()
