FROM jenkins/jenkins:2.267

ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
ENV CASC_JENKINS_CONFIG /var/jenkins_home/casc.yaml

ENV JENKINS_URL=
ENV JENKINS_NUM_EXECUTORS=2
ENV JENKINS_ADMIN_ID=admin
ENV JENKINS_ADMIN_PASSWORD=

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

COPY casc.yaml /var/jenkins_home/casc.yaml