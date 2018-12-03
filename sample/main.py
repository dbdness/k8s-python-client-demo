from kubernetes import client, config


def main():
    config.load_incluster_config()

    # Defining Pod
    v1 = client.CoreV1Api()
    pod = client.V1Pod()
    spec = client.V1PodSpec()
    pod.metadata = client.V1ObjectMeta(name="demo")

    # Defining container
    container = client.V1Container()
    container.image = "hello-world"
    # container.args = ["sleep", "3600"]
    container.name = "hello-world"

    # Assigning containers and spec to Pod
    spec.containers = [container]
    pod.spec = spec

    # Starting Pod
    print("Starting Pod...")
    print("Starting container with image '{0}'".format(container.image))
    v1.create_namespaced_pod(namespace="default", body=pod)
    print("Success!")


if __name__ == '__main__':
    main()
