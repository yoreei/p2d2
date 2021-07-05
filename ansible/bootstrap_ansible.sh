#!/bin/bash

## we execute the playbook in localhost mode

# scp -P 5001 ~/.ssh/* yordan@dorian.dima.tu-berlin.de:~/.ssh/
scp ~/.ssh/* ubuntu@ec2-3-125-39-227.eu-central-1.compute.amazonaws.com:~/.ssh/
scp ansible/* ubuntu@ec2-3-125-39-227.eu-central-1.compute.amazonaws.com:~/
ssh ubuntu@ec2-3-125-39-227.eu-central-1.compute.amazonaws.com sudo apt-get update
ssh ubuntu@ec2-3-125-39-227.eu-central-1.compute.amazonaws.com sudo apt-get -y install ansible
ssh ubuntu@ec2-3-125-39-227.eu-central-1.compute.amazonaws.com
