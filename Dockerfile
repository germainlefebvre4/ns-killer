FROM python:3-alpine

ARG KUBECTL_VERSION=1.13.11
ENV PYTHON_LOOP_FREQUENCY=10
ENV NS_PATTERN=".*"
ENV NS_RENTENTION_KIND="hours"
ENV NS_RENTENTION_TIME="1"

RUN apk update && apk add curl && \
    curl -Lo /usr/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    chmod +x /usr/bin/kubectl && \
    apk del curl

WORKDIR /usr/src/app
COPY . .
ENTRYPOINT [ "python", "./main.py" ]

