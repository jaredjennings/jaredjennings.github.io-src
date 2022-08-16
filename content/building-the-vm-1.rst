Building the VM
###############
:date: 2022-08-15 23:48
:author: jaredj
:category: Security
:tags: thehive, alpine, cortex, vm, training

I began to build a VM, using Alpine and `alpine-make-vm-image
<https://github.com/alpinelinux/alpine-make-vm-image>`_. At length I
succeeded, and began a repository of my own, starting from the example
files and building a Makefile to make the build nice. (To make the
build properly repeatable, it probably needs to run inside Docker, but
I'm not worrying about that yet. Also I'm not worrying about `Sigstore
<https://www.youtube.com/watch?v=KpyYVLHY8V8>`_ (17 min Youtube that I
have not yet watched) yet.

And I find that ``alpine-make-vm-image`` builds a hard drive image
with just the raw filesystem on it: no partition table of any kind, no
EFI system partition. How is it supposed to boot? When I create a
machine in ``virt-manager`` using this file as its hard drive, it
won't boot. Over to the issues of alpine-make-vm-image! And `behold
<https://github.com/alpinelinux/alpine-make-vm-image/issues/2>`_, I'm
trying to use xfs and that didn't work for someone else. Furthermore
after reading issue `#1
<https://github.com/alpinelinux/alpine-make-vm-image/issues/1>`_, it
seems the idea of adding partitions for bootability has already been
considered and rejected. And lo! using ext4 works properly. Syslinux
`supports XFS in an MBR partition
<https://wiki.syslinux.org/wiki/index.php?title=Filesystem#XFS>`_, and
seems to support Btrfs. I was thinking to use that, but it seems
someone `found in April
<https://blog.cubieserver.de/2022/dont-use-containerd-with-the-btrfs-snapshotter/>`_
that the special thing Btrfs can do to make containers go faster
actually makes them go slower, and it's been an unfixed issue for two
years. Ext4 it is, then!

This, though, is another difference between the minimal viable system
and one that will scale. The minimal system will have one node, k3s,
TheHive with SQLite storage, local indexing, and local attachment
storage; Cortex with whatever small storage it does; and
directory-based persistent volumes. The scalable one will have one or
more nodes, k3s, Longhorn, MinIO, Elasticsearch, ScyllaDB, and TheHive
and Cortex on top. A hypothetical Kubernetes operator could run the
database migration script to move minimal databases into scalable
ones. I'm not sure if there is a script to move attachments from local
storage to MinIO. The databases are easy to create using Kubernetes
custom resources and/or Helm charts, but there is nothing that would
cause them to exist. Also there is nothing that would create the
places for Longhorn to store things. Hmm, maybe Longhorn is
a necessary part of the minimal system. Hmm.
