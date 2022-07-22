learning about CoreOS Container Linux
#####################################
:date: 2017-01-25 00:16
:author: jaredj
:category: Home IT
:tags: security, coreos, containers, cloud
:slug: coreos-learning
:status: published

So the macvlan networking doesn't appear to work for me in the way I
had hoped. What I imagined CNI would get me was that each one of my
containers would get its own autoconfigured IPv6 address, and it would
be some Small Matter of Programming to get those addresses poked into
a DNS somewhere. But it seems all the container networking goodness of
CNI was really intended to let containers talk to each other: some
less-containerized, more-static, separate load balancer and/or reverse
proxy would sit in front, from what I'm gathering.

Bah, totally derailed, had to deal with
https://github.com/jaredjennings/puppet-mac_plist_value/issues/2. (Whaat,
someone is *using* my code? Wow!)

Ah - so I had a Docker nginx container running under rkt with macvlan,
and it could ping outward, and fetch things over the Web and such, but
it was trying to listen on port 80 and either sending RSTs to my SYN
packets, or dropping them. I made my own ACI container with acbuild
that just did an ``ip a`` to verify that it had the addresses by the
time code was running in the container, and then a ``nc -l -p
80``. Still no dice.

So I tried making my ``eth0`` in my CoreOS box be part of a bridge,
and making my containers be on the bridge network. It works for my
VMs, it ought to work for the containers. But now the CoreOS box can
ping out and fetch things, but not be pinged nor SSHed to.

I've found that the toolbox command in CoreOS exists, and also `found
<https://github.com/coreos/bugs/issues/1698>`_ that at the moment you
need to explicitly use Fedora 24 inside it not Fedora 25.

And I've found that CoreOS doesn't have ip6tables. And the first
result from a search for "ipv6 coreos" is "Guide for disabling ipv6."
Project Atomic isn't brimming with web pages about IPv6 either, but
Docker is being said to have some kind of IPv6 support. (The reader
should understand that IPv6 has been around for 25 years now, and I've
chosen to use it everywhere I can.)
