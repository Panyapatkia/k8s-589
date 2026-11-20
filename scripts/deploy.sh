#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "===== Kubernetes Deployment: ID-589 ====="

echo "[1] Apply Namespace"
kubectl apply -f k8s/00-namespace.yaml

echo "[2] Apply Storage"
kubectl apply -f k8s/01-storage.yaml

echo "[3] Apply About ConfigMap"
kubectl apply --server-side -f k8s/02-app-about-configmap.yaml

echo "[4] Deploy About"
kubectl apply -f k8s/02-app-about-deployment.yaml

echo "[5] Deploy Research"
kubectl apply -f k8s/03-app-research.yaml

echo "[6] Deploy API"
kubectl apply -f k8s/04-app-api.yaml

echo "[7] Apply Ingress"
kubectl apply -f k8s/05-ingress.yaml

echo "[8] Verify Resources"
kubectl get deployments,pods,svc -n id-589
kubectl get ingress -n id-589

echo "===== Deployment Completed ====="
