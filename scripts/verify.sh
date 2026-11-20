#!/bin/bash

echo "===== NODES ====="
kubectl get nodes -o wide

echo "===== NAMESPACE ====="
kubectl get ns id-589

echo "===== DEPLOYMENTS ====="
kubectl get deployments -n id-589

echo "===== PODS ====="
kubectl get pods -n id-589 -o wide

echo "===== SERVICES ====="
kubectl get svc -n id-589

echo "===== INGRESS ====="
kubectl get ingress -n id-589

echo "===== STORAGE ====="
kubectl get pv,pvc -n id-589

echo "===== ENDPOINTS ====="
kubectl get endpoints -n id-589

echo "===== INGRESS CONTROLLER ====="
kubectl get pods,svc -n ingress-nginx -o wide
