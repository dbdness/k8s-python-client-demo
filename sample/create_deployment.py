"""On-demand Kubernetes Deployment creation

This script creates a Deployment within the default Kubernetes cluster context.

This script also requires that `kubernetes` is installed within the Python
environment you are running this script in.

Variables:
    deployment_name (str): The desired deployment name
    replicas (int): Number of replicas
    pod_labels (dict{str:str}): Labels to assign to the Pod
    container_name (str): The desired name of the container
    container_image (str): The full path to the desired container image. Repository has to be included.
    container_port (int): The exposed port from within the Deployment.
"""

from kubernetes import client, config

deployment_name = "demo"
replicas = 1
pod_labels = {"app": "sentence-reverser"}
container_name = "sentence-reverser"
container_image = "registry.hub.docker.com/kimsen1992/sentence-reverser"
#container_image = "nginx:latest"
container_env_vars = [
    client.V1EnvVar(name="SENTENCE", value="Demo"),
    client.V1EnvVar(name="WEBHOOKURL",
                    value="https://webhook.site/e8d2c3a4-240c-44db-99df-82a7f5273117")
]
container_port = 80


# Loading default config
config.load_kube_config()
extension = client.ExtensionsV1beta1Api()

# Creating and defining Deployment object
deployment = client.ExtensionsV1beta1Deployment()
deployment.api_version = "extensions/v1beta1"
deployment.kind = "Deployment"
deployment.metadata = client.V1ObjectMeta(name=deployment_name)

# Defining Deployment spec with Pods
spec = client.ExtensionsV1beta1DeploymentSpec(
    template=client.V1PodTemplateSpec())
spec.replicas = replicas
spec.template.metadata = client.V1ObjectMeta(labels=pod_labels)
deployment.spec = spec

# Defining Pod container specs
container = client.V1Container(name=container_name)
container.image = container_image
container.env = container_env_vars
container.ports = [client.V1ContainerPort(container_port=container_port)]

# restart_policy options: "Always", "OnFailure", "Never"
spec.template.spec = client.V1PodSpec(containers=[container], restart_policy="OnFailure")

# Creating Deployment
print("Creating Deployment '{0}'".format(deployment_name))
extension.create_namespaced_deployment(namespace="default", body=deployment)
print("Success!")
