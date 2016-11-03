Compliance at home: Shortsighted
################################
:date: 2014-04-05 19:54
:author: jaredj
:category: Compliance at home, Projects, Security
:slug: compliance-at-home-shortsighted
:status: published

Two things happened to my compliance-at-home ideas this week:

1. Dave and Gunnar had a whole podcast episode about SCAP. I grudgingly
feel that it is cooler than I thought. The SCAP Security Guide project
in particular sounds like it is involving people from outside the
security area of expertise more than I thought. And part of the draw
toward contributing to SCAP content may be knowing your work will be
tool-neutral; any project I had started would be tool-specific.

2. In the course of `a Ruby FIPS
fix <https://bugs.ruby-lang.org/issues/9659>`__, I found that OpenSSL as
found in CentOS has had a lot of FIPS-related patches not seemingly
found in the upstream nor in Debian. If this is true in other packages
as well, it means making my Debian hosts at home as secure as my Red Hat
hosts at work is not merely a matter of configuration. A few months ago
I thought about setting up a `FreeIPA <http://freeipa.org>`__ server,
but was crestfallen to find RPM packaging baked into FreeIPA's build
process, such that it isn't easily usable in a Debian world. I thought
this was haughty. Maybe not?
