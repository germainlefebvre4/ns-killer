# Supported tags and respective `Dockerfile` links
* [latest](Dockerfile)

# Quick reference
* **Where to get help:**
the Docker Community Forums, the Docker Community Slack, or Stack Overflow

* **Where to file issues:**
[https://github.com/germainlefebvre4/k8s_ns-killer/issues](https://github.com/germainlefebvre4/k8s_ns-killer/issues)

* **Maintained by:**
[Germain LEFEBVRE](https://github.com/germainlefebvre4)

* **Supported architectures: (more info)**
amd64

* **Published image artifact details:**
repo-info repo's repos/k8s_ns-killer/ directory (history)
(image metadata, transfer size, etc)

* **Image updates:**

* **Source of this description:**
docs repo's docs/ directory (history)

# What is NS Killer?
A Kubernetes project to kill all namespace living over X times. Quite useful when auto-generated development environments on the fly and give them a lifecycle out-of-the-box from Kubernetes or even Helm.

# How to use this image
```sh
$ docker run -ti -d --name=ns-killer germainlefebvre4/k8s_ns-killer
```

# Parameters
| Parameter name | Description | Values | Default | Implemented? |
|---|---|---|---|---|
| PYTHON_LOOP_FREQUENCY | Define the time between 2 checks in secondes. | (integer) | 10 | Not yet |
| NS_PATTERN | Match your namespaces though a regex expression.  | (string) | - | Not yet |
| NS_RETENTION_KIND | Define the time unit. | days, hours, minutes | hours | Not yet |
| NS_RETENTION_TIME | Set the maximum lifetime of your namespace regarding the <kind> unit. | (integer) | - | Yes |


# Where to use this image
Let run this image in a Kubernetes cluster.

`001-namespace.yaml`
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ns-killer
```

`002-serviceaccount.yaml`
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ns-killer
  namespace: ns-killer
```

`003-clusterrolebinding.yaml`
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: ns-killer
  namespace: ns-killer
subjects:
- kind: ServiceAccount
  name: ns-killer
  namespace: ns-killer
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

`004-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ns-killer
  namespace: ns-killer
  labels:
    app.kubernetes.io/name: ns-killer
    app.kubernetes.io/ns-killer: ns-killer
    app.kubernetes.io/version: "1.0"
    app.kubernetes.io/managed-by: Germain
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: ns-killer
      app.kubernetes.io/ns-killer: ns-killer
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ns-killer
        app.kubernetes.io/ns-killer: ns-killer
    spec:
      serviceAccountName: ns-killer
      containers:
        - name: ns-killer
          image: "germainlefebvre4/k8s_ns-killer"
          #image: "eu.gcr.io/core-prof-social-pf-dsip/alpine:latest"
          imagePullPolicy: Always
          stdin: true
          tty: true
          env:
            - name: NS_PATTERN
              value: ".*"
            - name: NS_RETENTION_KIND
              value: "hours"
            - name: NS_RETENTION_TIME
              value: "1"
          resources:
            requests:
              cpu: 10m
              memory: 16Mi
```
