# DistributedSystemsArchitecture

Distributed Systems Architecture - project used for educational purposes. It consist of client which requests for stock prices. The server has 3 replicas and is implemented in Kubernetes cluster.

--->>>INSTRUCTIONS HOW TO RUN THE PROJECT<<<---
Guessing you have Docker Desktop insalled with Enabled Kubernetes:

// you must be in the directory of the dockerfile
docker build -t server-image:v1.0 .
note: note that the 'server-image:v1.0' should match the image in server-statefulset.yaml

// install nginx ingress controller in the kubernetes cluster
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.4/deploy/static/provider/cloud/deploy.yaml

// add the entry to your '/hosts' file
127.0.0.1 example.com
note: so when request is send to example.com -> it will go to localhost

// apply the config files to the cluster (you must be in the directory of the conf files - infra/k8s)
kubectl apply -f redis-depl.yaml
kubectl apply -f redis-service.yaml
kubectl apply -f server-statefulset.yaml
kubectl apply -f nginx-ingress-srv.yaml
// wait some time to get ingress-controller ready before running that one
kubectl apply -f nginx-ingress-controller.yaml

// see status of pods and services
kubectl get pods
kubectl get services
kubectl get pods -n ingress-nginx
kubectl logs <ingress-controller-pod-name> -n ingress-nginx

//containerize client and run a client
//you must be in the client directory
docker build -t client .
docker run --network host client
docker logs client
