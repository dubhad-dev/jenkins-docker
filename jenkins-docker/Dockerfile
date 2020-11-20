FROM jenkins/jenkins:lts

ARG DOCKER_COMPOSE_VERSION=1.27.4

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
      apt-transport-https \
      ca-certificates curl \
      gnupg-agent \
      software-properties-common \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    && apt-get update && apt-get install -y --no-install-recommends \
      docker-ce \
      docker-ce-cli \
      containerd.io \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

USER jenkins