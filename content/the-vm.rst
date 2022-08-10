TheHive virtual machine
#######################
:date: 2022-08-09 00:40
:author: jaredj
:category: Security
:tags: thehive, k3s, kubernetes, coreos, slem, k3os, terraform, ansible, packer, alpine

Prompt
------

TheHive has a "training VM." This is a built hard drive image that
contains an OS, with installed copies of TheHive, Cortex, and
MISP. I've never used it myself but I've heard of it.

As original maintenance of TheHive 4 falls off, that VM will stop
being updated, if it hasn't already. And if Kubernetes is going to be
as useful as I think it is, it should be both easy and increasingly
important to recreate that training VM using Kubernetes.

Audience
--------

When I want to demonstrate the software, I'll want this VM. I might
want it with the software already installed and ready to run,
depending on how much time there is to demonstrate.

People who just want to kick the tires will get this VM, and they
should be able to get up and running as quickly as possible. It might
be cool to watch the thing come up, download the containers, install
the software, and become healthy. But it would also be risky, take
time, and not be the reason you got the VM.

People setting up TheHive in a small company, or for a single
engagement, will want to start with this VM. It should not have
secrets baked into it. For this purpose, it should probably assemble
itself, but contain all the pieces, and maybe allow some configuration
from outside itself, somehow. (Adding organizational CAs, for example,
or indicating disk layouts.)

People setting up TheHive for their own team may be in a company where
they have to run a certain Linux distribution, because of management
and compliance concerns; and they might have to configure proxies or
add agents of some kind. They may even be under constraints as to
which Kubernetes distribution to run, or where to get artifacts such
as container images. They probably won't be able to start with this
VM, and that's OK.


Requirements
------------

So far, any Kubernetes should do, as long as you have ReadWriteMany
persistent volumes available to you and you can install Helm; but
*some* Kubernetes needs to be there, and whatever VM is built, people
will start to have questions about it, so it had better be
supportable. It needs a steady flow of easily installable updates as
well, to deal with security vulnerabilities.

Alternatives
------------

k3s is the one I've used so far and it's been quite good for
me. MicroK8s also exists, but I don't know of a good reason to switch,
and I trust Canonical less than SuSE, for some reason. (Where's Red
Hat? It appears they are not scaling this far down at the edge, but
running OpenShift there. OpenShift had much larger requirements last
time I checked... `yep
<https://docs.okd.io/latest/installing/installing_platform_agnostic/installing-platform-agnostic.html#installation-minimum-resource-requirements_installing-platform-agnostic>`_.)

For this iteration of my home container host, I've installed it on
Alpine Linux. I'm not sure what kind of pre-configuration Alpine may
support.

`SuSE Linux Enterprise Micro <https://www.suse.com/products/micro/>`_
is from the same people who bought Rancher, and therefore own k3s. But
I bet patches for it are part of what you pay for when you pay, and I
can't say what random people on the Internet may have paid money for.

`Fedora CoreOS <https://getfedora.org/coreos?stream=stable>`_ is a
candidate. It's been around for years, and probably will be for more
years. It has regular patches and a good story about how to apply
them. It is *extensively* configurable from before first boot, using
its Ignition system, and you can build those configurations into the
iso file. `A blog article
<https://www.murillodigital.com/tech_talk/k3s_in_coreos/>`_ about how
to do that... hmm, that would `work`, I guess, but it's already two
levels of YAML inclusion in one file, before we even start talking
about the Helm chart configurations to include. But it auto-patches!

Mmh. I can't do it man. I read about how Fedora CoreOS auto-updating
works, with zincati and rpm-ostree, how to roll back patches which
reminds me of FreeBSD/ZFS boot environments but reinvented differently
and complicated, and then I looked at the `alpine-make-vm-image
<https://github.com/alpinelinux/alpine-make-vm-image>`_ script, and
it's short and written in shell and I can understand the whole
thing. I'm already spending too many `innovation tokens
<https://mcfunley.com/choose-boring-technology>`_ on Kubernetes.

OK. So it's Alpine, with the files for a k3s airgap install (because
k3s makes up some secrets at install time) and a full complement of
container images, Helm charts, and values files prestaged. A custom
init script runs the k3s install on first boot, and k3s takes care of
the rest.
