Back at the helm
################
:date: 2022-07-04 22:48
:author: jaredj
:category: Security
:tags: kubernetes, helm, cortex, thehive

Last time I ran things with Docker and Kubernetes at home, it was a
couple of machines ago. Time to set up a new k3s machine.

I've got a virtual machine with two hard drives, one 50GB for the
system and one 400GB for data (mounted on /data), and 20GB of
RAM. I've installed the latest Alpine Linux on it, and unimaginatively
named it `k3s`. There are container-native distros like CoreOS, SuSE
Linux Enterprise Micro, or what have you, but I'm trying to start from
somewhere a little more neutral.

So I install k3s::

  mkdir -p /etc/rancher/k3s
  cat > /etc/rancher/k3s/config.yaml <<ITSOVER
  default-local-storage-path: "/data"
  ITSOVER
  wget -O get-k3s.sh https://get.k3s.io
  sh ./get-k3s.sh

Other prominent choices are MicroK8s and k0s; k3s has been good for
me. It's intended for production, and to be small enough to run on one
machine, but capable of scaling to a cluster. Operationally, it scales
down far enough to fit in my head, too. :)

Afterward I can ::

  k3s kubectl get node

and see my node is ready. At this writing, I've got version
1.23.8+k3s1. Now I can copy ``/etc/rancher/k3s/k3s.yaml`` off this
machine to my workstation, replace ``server: https://127.0.0.1:6443``
with ``server: https://k3s:6443`` (preserving indentation),
``sudo apt install kubernetes-client``, and then I can ::

  kubectl get node

from my workstation. I think this is the Kubernetes equivalent of
sshing as root, and I should have added a user instead; but I'm going
to forge ahead.

After a visit to https://helm.sh/, I've got a copy of Helm 3.9.0. Now
to my old blog articles to see what to do nex—oh my, ``kubectl`` sits
around for eight seconds every time I run it, that will not do.
