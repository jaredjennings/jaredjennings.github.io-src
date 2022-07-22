Building, etc., part 2
######################
:date: 2022-07-10 20:51
:author: jaredj
:category: Security
:tags: kubernetes, cortex, thehive, buildah, docker, podman

OK, so there's some trouble with Buildah, which I might have
anticipated. Cortex' build process expects to run Docker, not Buildah,
and while Buildah has all the same commands, Buildah's ``version``
subcommand doesn't take a ``--format`` switch. So I searched for other
ways. It seems there's this thing called Jib that will build your Java
application into a multi-layered container and doesn't need to use
Docker itself to do so. (This is unsurprising: the format for the
images is standardized at this point.) And Kaniko "is a tool to build
container images from a Dockerfile, inside a container or Kubernetes
cluster." Hey, that's where I'm at and where I want to go! But
apparently it `isn't supported as such
<https://github.com/sbt/sbt-native-packager/issues/1173>`_ in sbt.

OK. I've read up on the `Scala [2] tour
<https://docs.scala-lang.org/tour>`_, and watched a couple `videos
(Youtube) <https://www.youtube.com/watch?v=FS015lfyiMg>`_ about sbt,
and about Akka (`1 <https://www.youtube.com/watch?v=rIFqJxMJ1MM>`_, `2
<https://www.youtube.com/watch?v=xddHqIcnvHw>`_). I still don't like
Scala as well as someone who wants to start maintaining several Scala
codebases should, but maybe I'll be able to make some sense of it now.

