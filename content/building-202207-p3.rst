Building, etc., part 3
######################
:date: 2022-07-18 22:03
:author: jaredj
:category: Security
:tags: kubernetes, cortex, thehive, buildah, docker, podman

OK. I've learned: `sbt-native-packager` runs Docker to handle
container images of moderate complexity. There's an SBT Docker plugin
that goes a little deeper. `jib` and `kaniko` are tools that can build
images that aren't Docker, but they work rather differently.

The thing that presently blocks `sbt-native-packager` from using
Buildah instead is that the first thing it does is to run ``docker
version --format='...'``, and Buildah doesn't support the ``--format``
option. That might be a quick fix, but I should cave and use Docker
instead, because that's the current way to do it.

I'm trying in general not to make changes that require work, before
having managed to enlist other people interested in sharing said work,
and convincing them it's a good idea.

OK, so ::

    sudo apt remove podman
    sudo apt install docker.io

Aaand I have to mount the storage for the containers on
``/var/lib/docker`` instead of ``/var/lib/containers``. Stop the
docker, ``sudo mv /var/lib/docker /var/lib/docker.stock``, do the
switcheroo, now we have a large filesystem with all the right files
mounted on ``/var/lib/docker``. And this time I'll write it in my
``/etc/fstab``. As recommended, I use ``blkid`` to get the UUID of the
filesystem and use ``UUID=...`` as the source device, rather than the
name of a device file.

At length, I can build with Docker, except that node-sass doesn't run
because "Missing binding
/home/appuser/Cortex/www/node_modules/node-sass/vendor/linux_musl-x64-83/binding.node."
In other words, I can't use Alpine because it uses the smaller and
simpler musl instead of glibc. Okfine, we'll do Debian.

Some problems getting and building webpack; I find it's aptable and
add it. Some problems with css-spaces, preceded by bower not being
found. It's not aptable, but it is npmable. Aaand here's the winning
``Dockerfile.build-with-sbt`` this time around:

.. code:: Dockerfile

    FROM docker.io/adoptopenjdk/openjdk11-openj9:debian
    ENV SCALA_VERSION 2.12.14
    ENV SBT_VERSION 1.5.7

    RUN apt-get update
    RUN groupadd -g 5000 appuser && groupadd -g 130 docker && useradd -m -g 5000 -G 130 -u 5000 appuser
    RUN apt-get -y install bash openssl npm docker.io webpack
    RUN npm install -g bower
    USER appuser
    WORKDIR /home/appuser
    VOLUME /home/appuser/Cortex
    VOLUME /home/appuser/.ivy2
    VOLUME /home/appuser/.sbt
    VOLUME /home/appuser/.cache
    VOLUME /var/run/docker.sock

And I can run the build with

.. code:: sh

    sudo docker run -it \
        -v /build/Cortex:/home/appuser/Cortex \
        -v /build/dot-ivy2:/home/appuser/.ivy2 \
        -v /build/dot-cache:/home/appuser/.cache \
        -v /build/dot-sbt:/home/appuser/.sbt \
        -v /run/docker.sock:/var/run/docker.sock \
        ebf3963aa9e0 sh

Once in the container,

.. code:: sh

    cd Cortex
    ./sbt
    Docker/stage

And after that's through, the built binaries are staged in
``target/docker``, where I can cd to and ``sudo docker build .`` and
get an image! OK we are back to building Cortex.
