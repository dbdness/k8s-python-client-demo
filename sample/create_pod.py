"""On-demand Kubernetes "naked" Pod creation

This script creates a naked Kubernetes Pod - that is, a Pod that isn't controlled by any controller/resource.
The Pod and container within is defined by the various properties hard-coded into the Kubernetes library.

This script also requires that `kubernetes` is installed within the Python
environment you are running this script in.
"""

from kubernetes import client, config


config.load_kube_config()

# Defining Pod
v1 = client.CoreV1Api()
pod = client.V1Pod()
pod.metadata = client.V1ObjectMeta(name="demo")

# Defining container
container = client.V1Container(name="hello-world")
container.image = "hello-world"
# container.args = ["sleep", "3600"]

# Assigning container(s) and spec to Pod
spec = client.V1PodSpec(
    containers=[container],
    restart_policy="OnFailure")
pod.spec = spec

# Starting Pod
print("Starting Pod...")
print("Starting container with image '{0}'".format(container.image))
v1.create_namespaced_pod(namespace="default", body=pod)
print("Success!")
