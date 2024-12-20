# Scaling Operator for Kubernetes Operator

This repository contains a Kubernetes Operator designed to scale deployments based on custom schedules and scaling percentages. The Operator uses a Custom Resource Definition (CRD) to specify scaling behavior and runs a controller to manage the scaling logic.

## Features
- Automatically scales up deployments by a specified percentage at a scheduled time.
- Restores the deployment to its original state after a specified duration.
- Built for maintainability and ease of use.

## Requirements
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

## Development and Testing

### Local Development
To test the Operator locally, ensure your `KUBECONFIG` is properly set and run the Python script directly:
```bash
python python/main.py
```

### Dependencies
Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

### Required Files
- `k8s/scaling_crd.yaml`: Defines the custom resource schema.
- `k8s/deployment.yaml`: Deploys the Operator in the cluster.
- `k8s/service_account.yaml`: Service account for the Operator.
- `k8s/role.yaml`: Role with permissions for managing deployments.
- `k8s/role_binding.yaml`: Role binding to link the service account to the role.

### Testing

#### Run Tests
Use the `unittest` framework to validate the behavior of the Operator. Run the following command to execute the tests:
```bash
python -m unittest discover -s python -p "test_*.py"
```

#### Test Coverage
Tests are designed to mock Kubernetes API interactions and validate scaling behavior. Ensure that:
- CRDs are correctly processed.
- Deployments are scaled up and restored as expected.

#### Logs and Debugging
Enable verbose logging in the test suite by adding debug flags if needed.

## Known Limitations
- Assumes a namespace-scoped deployment model.
- Scaling behavior is dependent on accurate time synchronization in the cluster.

## Support
If you encounter any issues, please ensure the logs of the Operator are checked first. For additional assistance, contact the SRE team.

---

This Operator is built with maintainability in mind and can be handed off to any team for further development or enhancements.