Kubernetes early 2019
#####################
:date: 2019-04-11 19:12
:author: jaredj
:category: Projects

After several iterations of beginning to read the OpenShift Origin 3
(now OKD) documentation on installation, and being cowed by the system
requirements and the complexity, I've found a smaller way. This post
is for documenting what it is and why.

Hardware
--------

I obtained a used Dell desktop machine with a decently fast Intel
processor and 16GB of RAM. You can fit several virtual machines on
this that are the size of Raspberry Pis, without worrying about where
to physically put them, how to supply power, cooling and networking,
whether the USB 2.0 Ethernet will be good enough, how to provide
storage larger and more rewritable than SD cards, and whether you
should really get a different single-board computer instead, with SATA
and more RAM and real gigabit Ethernet and—oh wait it got expensive.

Rejected alternatives: `PicoCluster <https://www.picocluster.com>`_
(several SBCs available, including the Pine64), `MiniNodes
<https://www.mininodes.com/product/5-node-raspberry-pi-3-com-carrier-board/>`_. (Note
that neither of these comes with the single-board computers! They must
be purchased also.) Kubernetes instances in The Cloud.


Network
-------

I have a gigabit network with a consumer router running OpenWRT, and
several VLANs, none of which my cluster is going to cross at this
juncture. The router runs dnsmasq, which hands out DHCP addresses and
updates its DNS records to match. This works in fulfillment of
Kubernetes' requirement for working DNS servicing nodes.


Hypervisor
----------

Having procured a single large system, I had to split it up: taking
Kubernetes as an example, minikube is a thing, but is sort of
explicitly ephemeral and not for production; any real deployment has
to have at least three computers. Other technologies in the stack have
similar stories. I want to learn how they would be operated, not only
how to develop for them. By the same token I wanted my VMs to be
long-lived, subject to maintenance.

So I installed FreeBSD, which contains nothing unexpected. Its native
(and smallest) virtualization solution is bhyve. But I didn't want to
be running a bunch of ``bhyve --this-switch --that-switch &``, so I
found the vm-bhyve bhyve manager, which is a shell script. Simple,
small, no drama, works. I didn't like the way iohyve and chyves
structured their command line arguments.

Rejected alternatives: minikube, minishift, Vagrant-based
your-own-Kube-in-five-minutes gadgets, Xen, Fedora + kvm + libvirt
(which works well for me on another machine, with PCI VGA
passthrough).


Node operating system
---------------------

CoreOS has a very simple install (once I figured out how to pass it
the ssh key to accept using their more recent cloud-config
replacement). No choices. Dead simple upgrades. Made for
containers. Supported by kubespray (below). Bought by Red Hat, so it
has more of a certain future than CentOS Atomic. You have to boot the
CoreOS ISO with BIOS, but the installed OS with UEFI. Easy enough to
do, but hard to automate with vm-bhyve. You have to have 2GB of RAM to
boot the ISO. Inscrutable errors result otherwise.

Rejected alternatives: CentOS Atomic, CentOS, Debian, Ubuntu, Ubuntu
Core or whatnot. (Never got into the Ubuntu world. Ironic since I'm a
Debian adherent.)


Kubernetes install method
-------------------------

I wanted to learn what Kubernetes is and add on other stuff
myself. Kubespray is a set of Ansible playbooks (a tool I'm familiar
with) that can install Kubernetes on CoreOS. Nice. It took me a few
failures to figure out I needed 2GB RAM (again) on my master nodes,
though: the failure I got from Ansible did not lead me toward that
conclusion.

This was a difficult choice because everyone who's made a Kubernetes
distribution is quite proud of their work, but Kubernetes moves so
fast that what they were proud of six months ago may not even be a
thing anymore. But no one updates their page to say, "Well my dudes,
we got bought. Sayonara!" or whatnot.

Rejected alternatives: OKD, Ranchersomething, IBM's thing.


Network plugin
--------------

This one ferries packets that pods are sending to each other from one
node to the next. There are many choices, and Kubespray's expression
of them was the first concise comparison and contrast I've
seen. Calico was the default, and it looks to be the easiest given my
physical network setup.

Rejected alternatives: Flannel, Canal, Multus, Cisco ACI, etc., etc.


Load balancer
-------------

If you set up your Kubernetes cluster in the cloud, your cloud
provider provides this for you. Well, my cluster is on bare
metal. Imagine my surprise to find that MetalLB, which is made for the
purpose, is (a) beta, and (b) run by like one guy. But, like everyone
says, "it's working fine for me in production." I guess if you want
something that sounds less dodgy, you pony up for an F5 or something,
and hook your cluster up to it.


Ingress controller
------------------

The usual thing seems to be the Kubernetes nginx ingress controller. I
couldn't get that thing to work, but Traefik worked quite well for
me. Thanks to Traefik and MetalLB, I have some IP addresses running
name-based virtual hosting, so when I hook an A record up to them, I
can get to my application running inside Kubernetes. I dunno, maybe
the folks who set up Borg at Google and gained all that lovely domain
knowledge were not in charge of presenting me a web page when I visit
google.com, but whatever goes behind it... but actually making an
application visible outside the cluster was like five times as hard as
it should have been.

Rejected alternatives: well listed in Kubernetes documentation under
`Ingress Controllers
<https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/>`_;
I won't repeat the list here.


Storage
-------

I'm interested in running the usual sort of web apps on a Kubernetes
cluster: some code that stores some stuff in a database, or maybe some
files, and makes web pages that present that information. So I need
persistent storage. Now, it appears that here I have another choice
between simplicity and robustness: I could make a static set of
volumes and present them as persistent volumes to Kubernetes, or some
NFS shares, or whatnot. But the name of the game seems to be that when
you need to serve a service to the cluster, the coolest thing to do is
provide it from within the cluster, using some software that runs as
pods and presents an API, and (in this case) constructs the persistent
volumes needed at the time of request.

So Gluster can do this (with Heketi in front of it), but from what I
hear running a database on top of Gluster is a bad idea: it works best
for large, infrequent writes. Ceph may be better for
e.g. databases. And Rook, the API frontend that works with Ceph (among
others, like e.g. CockroachDB), looks nice, simple to set up, and has
an attractive website. Chosen.

Rejected alternatives: static NFS, Gluster.


Rook issues
-----------

Having configured Rook's cluster.yaml to my liking, I ran into
issues. First, the Kube cluster was initially unresponsive after first
putting up Rook. Not sure what happened there. Now the rook-ceph-agent
pod won't start because ``error while creating mount source path
'/usr/libexec/kubernetes/kubelet-plugins/volume/exec': mkdir
/usr/libexec/kubernetes: read-only file system``. This is because I'm
using CoreOS, and its /usr is mounted read-only, I reckon. Part of the
magic updates. I found some `guidance
<https://github.com/rook/rook/blob/master/Documentation/tectonic.md>`_
on running Rook on CoreOS Container Linux. Although it is intended for
people running Tectonic Kubernetes, it has a guide for moving the
place where the volume plugins go by modifying the systemd service
file for the kubelet.

Oh interesting, the kubelet startup as put in place by kubespray
already has this sort of thing in it. But the rook-ceph-agent
container (image rook/ceph:master, id
``docker-pullable://rook/ceph@sha256:92a72f2f2883c79137d4ac771b2c646683aaa39874dc5e7fc9e78463f47a547f``)
is still trying to make that directory.


The rest
--------

is not written yet.
