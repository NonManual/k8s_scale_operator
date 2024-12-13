## What this app does?
This application is a Kubernetes Operator designed to dynamically scale deployments based on custom schedules and scaling percentages. It provides:

- A Custom Resource Definition (CRD) to specify scaling configurations.
- Controller logic to monitor and apply scaling events at defined times.
- Integration with Kubernetes deployments to scale up or down resources temporarily.

Key features:
- Automatically adjusts deployment replicas based on a schedule.
- Restores deployments to their original state after the scaling period ends.
- Designed for maintainability and extensibility.

---
## Setup
### 1. Deploy the CRD
The Custom Resource Definition (CRD) defines the schema for the custom resource `ScalingResource`.

Run the following command to deploy the CRD:
```bash
kubectl apply -f k8s/scaling_crd.yaml
```

### 2. Deploy the Operator
The Operator runs as a Deployment in your Kubernetes cluster. Apply the necessary manifests:

```bash
kubectl apply -f k8s/service_account.yaml
kubectl apply -f k8s/role.yaml
kubectl apply -f k8s/role_binding.yaml
kubectl apply -f k8s/deployment.yaml
```

### 3. Define Scaling Resources
Create a custom resource to define the scaling behavior for your deployment. Below is an example manifest:

```example_scaling_resource.yaml
apiVersion: teamsnap.com/v1
kind: ScalingResource
metadata:
  name: example-scaling
  namespace: default
spec:
  scalePercentage: 20  # Scale up by 20%
  scheduleTime: "08:50"  # Start scaling at 8:50 AM
  duration: "30"  # Duration in minutes
  targetDeployment: "web-server-deployment"  # Name of the deployment to scale
```

Apply the custom resource using `kubectl`:
```bash
kubectl apply -f example_scaling_resource.yaml
```

### 4. Monitor the Operator
Check the logs of the Operator to ensure it is running correctly:
```bash
kubectl logs -l app=scaling-operator
```

### 5. Verify Scaling
The Operator will scale the target deployment according to the specified schedule and restore the original replicas after the specified duration. Verify the scaling by inspecting the deployment:
```bash
kubectl get deployment web-server-deployment
```
### Dependencies
Install the required Python dependencies:
```bash
pip install -r requirements.txt
```
- Kubernetes cluster (v1.20+ recommended)
- Python 3.7+
- `kubectl` configured for the target cluster
- `kubernetes` Python client

## Setup Instructions

### 1. Deploy the CRD
The Custom Resource Definition (CRD) defines the schema for the custom resource `ScalingResource`.

Run the following command to deploy the CRD:
```bash
kubectl apply -f k8s/scaling_crd.yaml
```

### 2. Deploy the Operator
The Operator runs as a Deployment in your Kubernetes cluster. Apply the necessary manifests:

```bash
kubectl apply -f k8s/service_account.yaml
kubectl apply -f k8s/role.yaml
kubectl apply -f k8s/role_binding.yaml
kubectl apply -f k8s/deployment.yaml
```

### 3. Define Scaling Resources
Create a custom resource to define the scaling behavior for your deployment. Below is an example manifest:

```example_scaling_resource.yaml
apiVersion: teamsnap.com/v1
kind: ScalingResource
metadata:
  name: example-scaling
  namespace: default
spec:
  scalePercentage: 20  # Scale up by 20%
  scheduleTime: "08:50"  # Start scaling at 8:50 AM
  duration: "30"  # Duration in minutes
  targetDeployment: "web-server-deployment"  # Name of the deployment to scale
```

Apply the custom resource using `kubectl`:
```bash
kubectl apply -f example_scaling_resource.yaml
```

### 4. Monitor the Operator
Check the logs of the Operator to ensure it is running correctly:
```bash
kubectl logs -l app=scaling-operator
```

### 5. Verify Scaling
The Operator will scale the target deployment according to the specified schedule and restore the original replicas after the specified duration. Verify the scaling by inspecting the deployment:
```bash
kubectl get deployment web-server-deployment
```

##  Development
To test the Operator locally, ensure your `KUBECONFIG` is properly set and run the Python script directly:
```bash
python python/main.py
```
## Testing

### Run Tests
Use the `unittest` framework to validate the behavior of the Operator. Run the following command to execute the tests:
```bash
python -m unittest discover -s python -p "test_*.py"
```

### Test Coverage
Tests are designed to mock Kubernetes API interactions and validate scaling behavior. Ensure that:
- CRDs are correctly processed.
- Deployments are scaled up and restored as expected.