#!/usr/bin/env python

import os
import signal
import subprocess
import sys
import time

import requests
from api4jenkins import Jenkins
from api4jenkins.node import Node, Nodes
from api4jenkins.system import System

process = None


def signal_handler(sig, frame):
    if process != None:
        process.send_signal(signal.SIGINT)


def is_master_ready(jenkins_url: str) -> bool:
    try: 
        return requests.head(f"{jenkins_url}/login").status_code == 200
    except:
        return False


def create_node(jenkins: Jenkins, name: str, labels: str, working_dir: str, num_executors: int):
    Nodes(jenkins, f"{jenkins.url}/computer").create(
        name=name,
        labelString=labels,
        remoteFS=working_dir,
        numExecutors=num_executors
    )


def get_node(jenkins: Jenkins, name: str) -> Node:
    return Nodes(jenkins, f"{jenkins.url}/computer").get(name)


def get_secret(jenkins: Jenkins, name: str) -> str:
    return System(jenkins, jenkins.url).run_script(f'jenkins.model.Jenkins.getInstance().getComputer("{name}").getJnlpMac()').split()[1]


def run_node(jenkins_url, name, secret, working_dir, jar_path="/usr/share/jenkins/agent.jar"):
    params = ['java', '-classpath', jar_path, 'hudson.remoting.jnlp.Main',
              '-headless', '-url', jenkins_url, '-workDir', working_dir, secret, name]
    return subprocess.Popen(params, stdout=subprocess.PIPE)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    jenkins_url = os.environ['JENKINS_URL']
    jenkins_user = os.environ['JENKINS_USER']
    jenkins_password = os.environ['JENKINS_PASS']
    jenkins_wait_interval = int(os.environ['JENKINS_WAIT_INTERVAL'])

    node_name = os.environ['NODE_NAME']
    if not node_name:
        node_name = f"docker-node-{os.environ['HOSTNAME']}"
    node_labels = os.environ['NODE_LABELS']
    node_num_executors = int(os.environ['NODE_NUM_EXECUTORS'])
    node_working_dir = "/home/jenkins"

    while not is_master_ready(jenkins_url):
        print("Master is not ready")
        print(f"Waiting {jenkins_wait_interval} seconds")
        time.sleep(jenkins_wait_interval)
    print("Master is ready")

    jenkins = Jenkins(jenkins_url, auth=(
        jenkins_user, jenkins_password), token=True)
    if not jenkins.exists():
        sys.exit("Master is not running! Exiting...")
    print(f"Master is up and running (Jenkins v{jenkins.version})")

    create_node(jenkins, name=node_name, labels=node_labels,
                working_dir=node_working_dir, num_executors=node_num_executors)
    node = get_node(jenkins, name=node_name)
    print(f"Node {node_name} created on master using working dir \"{node_working_dir}\" and {node_num_executors} executors with labels: \"{node_labels}\"")

    secret = get_secret(jenkins, name=node_name)
    process = run_node(jenkins_url, name=node_name,
                       secret=secret, working_dir=node_working_dir)
    print(f"Node {node_name} running")
    process.wait()

    node.delete()
    print(f"Node {node_name} removed")
