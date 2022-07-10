Building containers with Scala and Play software, July 2022, part 1
###################################################################
:date: 2022-07-06 20:16
:author: jaredj
:tags: kubernetes, cortex, thehive, buildah, docker, podman

I've done some work to update my Cortex `pull request
<https://github.com/TheHive-Project/Cortex/pull/349>`_ for Kubernetes
support. Now I need to see if it builds. Last time, I tried several
times to come up with a working build environment for Cortex, and
ended up summoning one using Docker. This time, I'm going to use
Podman and Buildah, although rootless Podman looks tedious enough that
I won't do it right now, considering some time pressure I'm
feeling. Technically it could all happen in a Kubernetes Job, but I'm
not going to set up continuous integration just yet. One of the
complaints I've heard is that it is inscrutable how to build this
software, so I want to write that down better for people first, then
machines.

As before, I'll make up odd names for things I create, and if you are
copying and pasting along, and you see one of these names, you'll want
to replace it with something that makes sense in your context.

volgrop
    An LVM volume group.
contnrs
    A logical volume for storing container-related files.

So I begin on my Debian unstable workstation by

.. code:: sh

    sudo apt install podman containers-storage
    sudo lvcreate -L 150G -n contnrs volgrop
    sudo mkfs.ext4 /dev/volgrop/contnrs
    cd /var/lib
    sudo mv containers containers.stock
    sudo mkdir containers
    sudo mount /dev/volgrp/contnrs containers
    sudo chmod --reference=containers.stock containers
    sudo rsync -av containers.stock/ containers/
    sudo rm -rf containers.stock

Now I'll get my local copies of things ready. I found out previously
that to mount the Cortex source directory as a volume inside a
container, I needed a locally stored copy. And all the packages
fetched by sbt (and built, maybe?) were stored in ``$HOME/.ivy2``,
``$HOME/.sbt`` and ``$HOME/.cache``. Keeping those across build
invocations saves a lot of time, so there's more volumes to mount
inside the build container. I made another logical volume and
filesystem, mounted at ``/build``. Here's my
``Dockerfile.build-with-sbt`` this time:

.. code:: Dockerfile

    # If I don't use JDK 11, a message says that Play only supports
    # JDK 8, 11, and experimentally 17. So let's do 11. And the OpenJ9
    # version because I feel saucy. And we'll give it a fully qualified
    # name because buildah doesn't assume you are using docker.io like
    # Docker does. That is good. If it required a whole URL, without a
    # non-standard URL scheme, it would be even better...
    FROM docker.io/adoptopenjdk/openjdk11-openj9:x86_64-debian-jdk-11.0.11_9_openj9-0.26.0
    ENV SCALA_VERSION 2.12.14
    ENV SBT_VERSION 1.5.7

    RUN \
    apt-get update && apt-get -y install npm webpack
    RUN groupadd -g 5000 appuser && useradd -m -g 5000 -u 5000 appuser
    USER appuser
    WORKDIR /home/appuser
    VOLUME /home/appuser/Cortex
    VOLUME /home/appuser/.ivy2
    VOLUME /home/appuser/.sbt
    VOLUME /home/appuser/.cache

This time around I notice sbt's ``~`` command to do a thing when
source files change. The errors aren't getting grokked by Emacs, so I
can't warp right to where they are, but the build is nice and fast. ::

    [cortex] $ ~ Docker/stage

Now I've got an ELIFECYCLE, and a warning that npm doesn't support
Node 10. And it can't find the version of Docker, because there is no
docker.io package installed inside the container. Oh and this is still
all about Cortex because that's what I've built before. I have not
tried to build TheHive yet. But it ought to go about the same, right?
To be continued...

