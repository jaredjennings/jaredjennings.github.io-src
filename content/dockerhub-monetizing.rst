DockerHub monetizing
####################
:date: 2023-03-17 18:48
:author: jaredj
:category: Somebodyoughta

Just caught the news of DockerHub making some moves unfriendly to
open-source projects, on `Linux Action News 284`_. This is supposed to
go to show the dangers of centralization.

.. _`Linux Action News 284`: https://www.jupiterbroadcasting.com/show/linux-action-news/284/

People are fleeing to some GitHub-provided container repo, which of
course is no less centralized; but also were we all not `giving up
GitHub`_ a minute ago because they made a code-plagiarizing machine?
The problem is that our tools are defining new, centralized
namespaces: ``docker`` did not use URLs to locate container images,
but paths hardcoded to begin at a name belonging to Docker. Was the
momentarily superior developer experience of not typing 'https://' a
few times worth the worry we now feel? But ``docker`` was made by
Docker, and they were at some early time the only place hosting
container images that would work with ``docker``. I still felt
squeamish when the whole actual location wasn't written out. Every
tool after that of course had to work like ``docker`` for all the
preexisting cases; but we could have had a linter somewhere that would
urge you to use real URLs.

.. _`giving up GitHub`: https://sfconservancy.org/blog/2022/jun/30/give-up-github-launch/

And where people are building tools that take `username/reponame` and
assume it means https://github.com/username/reponame, when those
people don't even work for GitHub—well, we should know better. Even
assuming the use of Git is centralizing too much, I think. What if I
want to use Pijul or Fossil or Darcs?

Anyway what I set out to say is if we really want to decentralize
container images, why not `use IPFS?`_ It doesn't matter where you get
it from if it's `signed`_, and good citizens can be mirrors without
much of any extra effort. Various kinds of security checks, which are
often stuck to container registries as far as I know, could also be
decentralized: like `OpenBadges`_, but for container images not
people. (This paragraph has been brought to you by cryptographic
hashes and digital certificates.)

.. _`use IPFS?`: https://github.com/ipdr/ipdr
.. _`signed`: https://www.sigstore.dev/
.. _`OpenBadges`: https://openbadges.org/
