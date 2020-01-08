FROM python:3.7-slim-stretch AS base

ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT


FROM base as builder

RUN apt update && \
    apt install -y python-pip && \
    apt -y clean && \
    pip install pipenv

# Update pipenv libs
COPY Pipfile* ./
RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy --ignore-pipfile


FROM base

ARG KUBECTL_VERSION=1.14.10

# Kubectl
RUN apt update && apt install -y curl && \
    curl -Lo /usr/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x /usr/bin/kubectl

# Python libs and sources
COPY --from=builder $PYROOT/lib/ $PYROOT/lib/
COPY rentalcar-requests.py .

CMD ["python", "main.py"]
