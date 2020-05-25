# launch instance:
#. ./openrc.sh; ansible-playbook -i ./inventory/hosts.ini --ask-become-pass instance.yaml

# Deploy data server:
#ansible-playbook -i ./inventory/hosts.ini --ask-become-pass dataserver.yaml

# Deploy web server:
ansible-playbook -i ./inventory/hosts.ini --ask-become-pass webserver.yaml

# Harvest twitter
#ansible-playbook -i ./inventory/hosts.ini --ask-become-pass Harvest.yaml



#!/usr/bin/env bash
