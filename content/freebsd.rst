FreeBSD
#######
:date: 2017-04-09 00:19
:author: jaredj
:category: Home IT
:slug: freebsd
:status: published

So `this issue
<https://github.com/containernetworking/cni/issues/245>`_ has gotten
some comments, but no fixes. Meanwhile I've been listening to the `BSD
Now <http://bsdnow.tv/>`_ podcast. I decided to give FreeBSD a go.

On BSDs you have jails not usually containers. Docker exists for
FreeBSD, but I decided to find out what the flap about jails is. I was
shocked to find that when you create a jail you have to give it an
IPv6 address if you want it to have one. I tried using vnet to give it
a whole network stack instead of just an IP address, but it didn't
autoconfigure. Perhaps this is possible using one of the many arcane
flags to ``ifconfig`` (which truly feels like a throwback after using
``ip``), but I didn't find it, and I did find that to this day vnet is
crashing people's FreeBSD boxen.

Upon contemplation I realized this is much simpler. The issue linked
above is about how to get an IPv6 address for a container and then
make sure that address is known wherever it needs to be (DNS, other
containers, etcd, or whatnot). This is important when you don't want
to pay individual attention to a container. But what I'm finding is
that at the scale I'm operating at (one node, dozens of containers at
most), it wouldn't kill me to configure an IP address, and then I'd
know it ahead of time.

After being revolted by dbus, NetworkManager, systemd and their
dynamic ilk, and eventually getting used to them, it's odd to go
back. But I'm trying it.
