FROM python:3.7-alpine AS base

ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT


FROM base as builder

RUN apk update && \
    apk add --no-cache py-pip && \
    pip install pipenv

# Update pipenv libs
COPY Pipfile* ./
RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy --ignore-pipfile


FROM base

ARG KUBECTL_VERSION=1.14.10

# Kubectl
RUN apk update && \
    apk add curl && \
    curl -Lo /tmp/kubernetes-client-linux-amd64.tar.gz https://dl.k8s.io/v${KUBECTL_VERSION}/kubernetes-client-linux-amd64.tar.gz && \
    tar -zxvf /tmp/kubernetes-client-linux-amd64.tar.gz -C /tmp && \
    mv /tmp/kubernetes/client/bin/kubectl /usr/bin/kubectl && \
    chmod +x /usr/bin/kubectl

# Python libs and sources
COPY --from=builder $PYROOT/lib/ $PYROOT/lib/
COPY . .

CMD ["python", "handler.py"]
