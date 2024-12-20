from kubernetes import client, config
from datetime import datetime, timedelta
import time

# Load Kubernetes configuration from the default location or environment variables
config.load_kube_config()

# Controller Logic for managing scaling of Kubernetes resources based on CRD specifications
def scale_resource():
    # API for interacting with custom resources
    api = client.CustomObjectsApi()
    # API for interacting with Kubernetes deployments
    v1_apps = client.AppsV1Api()

    while True:
        # Retrieve all instances of the custom resource "ScalingResource" in the default namespace
        crds = api.list_namespaced_custom_object(
            group="teamsnap.com",  # Custom resource group
            version="v1",  # Version of the CRD
            namespace="default",  # Namespace where the CRD instances are defined
            plural="scalingresources"  # Plural name of the custom resource
        )

        # Iterate over each instance of the custom resource
        for item in crds.get('items', []):
            spec = item['spec']  # Extract the specification of the custom resource
            deployment_name = spec['targetDeployment']  # Name of the target deployment to scale
            scale_percentage = spec['scalePercentage']  # Percentage to scale the replicas
            schedule_time = datetime.strptime(spec['scheduleTime'], "%H:%M")  # Scheduled time for scaling
            duration = timedelta(minutes=int(spec['duration']))  # Duration for scaling up
            current_time = datetime.now().time()  # Current time for comparison

            # Check if the current time falls within the scaling schedule window
            if schedule_time.time() <= current_time <= (schedule_time + duration).time():
                # Retrieve the current deployment configuration
                deployment = v1_apps.read_namespaced_deployment(deployment_name, "default")
                original_replicas = deployment.spec.replicas  # Store the original number of replicas

                # Calculate the new number of replicas based on the scaling percentage
                new_replicas = int(original_replicas * (1 + scale_percentage / 100))

                # Apply the scaling to the deployment
                deployment.spec.replicas = new_replicas
                v1_apps.replace_namespaced_deployment(deployment_name, "default", deployment)

                # Wait for the specified duration before scaling back down
                time.sleep(duration.total_seconds())

                # Restore the original number of replicas
                deployment.spec.replicas = original_replicas
                v1_apps.replace_namespaced_deployment(deployment_name, "default", deployment)

        # Wait for a minute before checking the custom resources again
        time.sleep(60)

if __name__ == "__main__":
    # Entry point: Start the scaling controller logic
    scale_resource()
