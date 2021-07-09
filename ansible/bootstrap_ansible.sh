#!/bin/bash

## we execute the playbook in localhost mode

# scp -P 5001 ~/.ssh/* yordan@dorian.dima.tu-berlin.de:~/.ssh/
IP="ec2-18-197-150-40.eu-central-1.compute.amazonaws.com"

scp ~/.ssh/* ubuntu@"${IP}":~/.ssh/
scp ansible/* ubuntu@"${IP}":~/
ssh ubuntu@"${IP}" sudo apt-get update
ssh ubuntu@"${IP}" sudo apt-get -y install ansible
ssh ubuntu@"${IP}"
