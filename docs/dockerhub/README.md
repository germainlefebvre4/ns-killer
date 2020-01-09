# Supported tags and respective `Dockerfile` links
* [latest](Dockerfile)

# Quick reference
* **Where to get help:**
the Docker Community Forums, the Docker Community Slack, or Stack Overflow

* **Where to file issues:**
[https://github.com/germainlefebvre4/ns-killer/issues](https://github.com/germainlefebvre4/ns-killer/issues)

* **Maintained by:**
[Germain LEFEBVRE](https://github.com/germainlefebvre4)

* **Supported architectures: (more info)**
amd64

* **Published image artifact details:**
repo-info repo's repos/ns-killer/ directory (history)
(image metadata, transfer size, etc)

* **Image updates:**

* **Source of this description:**
docs repo's docs/ directory (history)

# What is NS Killer?
A Kubernetes project to kill all namespace living over X times. Quite useful when auto-generated development environments on the fly and give them a lifecycle out-of-the-box from Kubernetes or even Helm.

# How to use this image
```sh
$ docker run -ti -d --name=ns-killer germainlefebvre4/ns-killer
```

# Parameters
| Parameter name | Description | Values | Default | Implemented? |
|---|---|---|---|---|
| NS_PATTERN | Match your namespaces though a regex expression.  | (string) | - | Not yet |
| NS_RETENTION_KIND | Define the time unit. | months, days, hours, minutes | hours | Yes |
| NS_RETENTION_TIME | Set the maximum lifetime of your namespace regarding the <kind> unit. | (integer) | - | Yes |


# Where to use this image
Let's run this image in a Kubernetes cluster.

Kubernetes manifest are present in directory [kubernetes/](kubernetes).