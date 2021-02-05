FROM python:3.7-alpine AS base
ARG KUBECTL_VERSION=1.14.10

# Kubectl
RUN apk update && \
    apk add curl && \
    curl -Lo /tmp/kubernetes-client-linux-amd64.tar.gz https://dl.k8s.io/v${KUBECTL_VERSION}/kubernetes-client-linux-amd64.tar.gz && \
    tar -zxvf /tmp/kubernetes-client-linux-amd64.tar.gz -C /tmp && \
    mv /tmp/kubernetes/client/bin/kubectl /usr/bin/kubectl && \
    chmod +x /usr/bin/kubectl

COPY Pipfile* .

RUN apk update && \
    apk add --no-cache py-pip && \
    pip install pipenv && \
    pipenv lock --requirements > requirements.txt && \
    pip install -r requirements.txt

COPY . .

# Kubectl
RUN apk update && \
    apk add curl && \
    curl -Lo /tmp/kubernetes-client-linux-amd64.tar.gz https://dl.k8s.io/v${KUBECTL_VERSION}/kubernetes-client-linux-amd64.tar.gz && \
    tar -zxvf /tmp/kubernetes-client-linux-amd64.tar.gz -C /tmp && \
    mv /tmp/kubernetes/client/bin/kubectl /usr/bin/kubectl && \
    chmod +x /usr/bin/kubectl

CMD ["/bin/sh", "entrypoint.sh"]
