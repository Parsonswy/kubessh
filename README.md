# KubeSSH
This project was originally developed by [yuvipanda on GitHub](https://github.com/yuvipanda/kubessh).

KubeSSH is a connection broker for pods in Kubernetes. The primary usecase which drives development philosophy is on-demand infrastructure for development environments. When a user sucesfully connects to KubeSSH, a pod is provisioned and the user connected to a bash process in that pod. From there the user is free to do as they please within the container. This is more flexible than a VM as time required to provision, maintain, or reset a container is much lower than a full VM. Terminal pods can be quickly provisioned or torne down to meet user demand.

Putting each user in their own Kubernetes Pod has several advantages over traditional terminal servers.
1. Users can use different container images, providing a large amount of flexibility in what
   software is available. No waits for admins to install specific packages, or conflicts
   with packages needed by other users.
2. Strong resource guarantees (CPU, RAM, GPUs, etc) prevent users from exhausting resources
   on any single login node.
3. Can scale dynamically to a very large number of simultaneous users.
4. Authentication and Authorization can be much more dynamic, since we are no longer
   tied to the traditional POSIX model of user accounts. For example, you can allow
   users to log in via OAuth2 / OpenID Connect providers!
5. Provide access to kubernetes API for users to run jobs and do all the cool things
   Kubernetes can do, without having to set up `kubectl` and friends on their local
   computers.

# Project Status

This fork of KubeSSH has recently been spawned by the [Networking and Computing Student Association at Michigan Technological University](https://ncsa.tech/). There are several changes and expansions we'd like to this project, but don't have a specific timeline for those changes at this time.
```
- LDAP(s) Authentication // Partially implemented.
- Support different container images for different users.
- Support different pod templates for different users.
- Support multiple active pods for a single user. // Right now the username is tied to the pod name so each user only gets 1 pod.
- Administrative interface. This would likley be a webpage that would make doing several of the above features much easier.
- Documentation and resources describing security considerations when giving users terminal access to your cluster.
```
> Alot of these features just seem like things you can do with kubectl. Why use KubeSSH?

Again, our primary usecase for KubeSSH is development environments. Building these mechanisms into KubeSSH allows developers and engineers to utilize cluster compute power without hours of learning how to deploy in Kubernetes. This is especially useful in an educational environment when paired with tools like VSCode and Okteto. An entire development stack can be templated out by a more experienced developer and devs new to the project can jump right into development without having to worry about how to setup Mongo, MySQL, Node, Redis, RabbitMQ, etc.

# Installation
At this time we don't have an official build or container image available. You can build your own image using Python 3.8.
```
git clone https://github.com/Parsonswy/kubessh.git
cd kubessh
python3.8 -m pip install -r requirements.txt # Install dependencies
kubessh --KubeSSH.config_file=[path to config.py]
```

See `kubessh/app.py` and `kubessh/authentication/[provider you want to use].py` for configuration options.
```python
# Example config that uses LDAP[S] for authentication
from kubessh.authentication.ldap import LDAPAuthenticator

# Make sure this exists
c.KubeSSH.host_key_path = 'dummy-kubessh-host-key'

c.KubeSSH.debug = True
c.KubeSSH.authenticator_class = LDAPAuthenticator
c.KubeSSH.authenticator_class.ldap_servers = [ 'dc01.ncsa.tech', 'dc02.ncsa.tech' ]
```

# Legacy Documentation & Notes

The below resources may still be useful for anyone looking into this project, but are not affiliated with this fork. These resources were published and maintained by the origianl project owner. Until we are able to port our own official docs over to this fork, we link these as a resource and will do a our best to indicate where changes invalidate them. These resources may also disappear at anytime and there is nothing we can do about that.

[![Documentation Status](https://readthedocs.org/projects/kubessh/badge/?version=latest&style=flat)](https://docs.kubessh.org)


KubeSSH brings the familiar SSH experience to a modern cluster manager.

> I have some code that requires more RAM / CPU / GPUs / Network / Time to run than my laptop can offer.
> What is the simplest, most user friendly way to run this code?

KubeSSH is an experiment in trying to answer this question.

