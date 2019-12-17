FROM python:3-alpine

ARG KUBECTL_VERSION=1.14.10

RUN apk update && apk add curl && \
    curl -Lo /usr/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x /usr/bin/kubectl && \
    apk del curl

WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "./main.py" ]

