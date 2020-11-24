FROM python:3.9.0
ENV PYTHONUNBUFFERED=1

ARG API_VERSION=4.6
ARG DOCKER_COMPOSE_VERSION=1.27.4

ENV JENKINS_URL=
ENV JENKINS_USER=
ENV JENKINS_PASS=
ENV JENKINS_WAIT_INTERVAL=10
ENV NODE_NAME=
ENV NODE_LABELS=docker
ENV NODE_NUM_EXECUTORS=2

RUN apt-get update && apt-get install -y --no-install-recommends \
      default-jre \
    && rm -rf /var/lib/apt/lists/*

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

RUN curl --create-dirs -fsSLo /usr/share/jenkins/agent.jar https://repo.jenkins-ci.org/public/org/jenkins-ci/main/remoting/${API_VERSION}/remoting-${API_VERSION}.jar \
  && chmod 755 /usr/share/jenkins \
  && chmod 644 /usr/share/jenkins/agent.jar \
  && ln -sf /usr/share/jenkins/agent.jar /usr/share/jenkins/slave.jar

RUN pip install --no-cache-dir api4jenkins

COPY agent.py /usr/share/jenkins/agent.py

RUN mkdir -p /home/jenkins

WORKDIR /home/jenkins

CMD [ "python", "/usr/share/jenkins/agent.py" ]