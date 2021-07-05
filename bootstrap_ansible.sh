#!/bin/bash

## we execute the playbook in localhost mode

# scp -P 5001 ~/.ssh/* yordan@dorian.dima.tu-berlin.de:~/.ssh/
scp ~/.ssh/* ubuntu@ec2-3-125-39-227.eu-central-1.compute.amazonaws.com:~/.ssh/
scp site.yml ubuntu@ec2-3-125-39-227.eu-central-1.compute.amazonaws.com:~/
ssh ubuntu@ec2-3-125-39-227.eu-central-1.compute.amazonaws.com
