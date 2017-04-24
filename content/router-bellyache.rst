router bellyache
################
:date: 2017-04-21 23:22
:author: jaredj
:category: Commentary
:tags: somebodyoughta
:slug: router-bellyache
:status: published

I have a router that runs LEDE. It has 115 firewall rules. I made
these by typing stanzas of about eight lines each into a file
`/etc/config/firewall`. Not great, not bad. I've already `held forth
</netconf-and-the-curse-of-consensus.html>`_ on this some. But now the
path of least resistance for deploying web apps on my own
infrastructure seems to be to create jails on a FreeBSD system
(statically setting their IPv6 addresses), (security hardening
handwaving), and add a firewall rule to allow access to a jail from
some zone (e.g. my LAN, the Internet). This is now an orchestratey
kind of task. And in between my earlier rant and now, I've used
Ansible some.

There's an Ansible role to set the firewall configuration on an
OpenWRT router—but it only sets the entire configuration. To do this
orchestratey task, I would need to use ``uci`` to make the edit. But
``uci``, when you are setting something like a firewall rule, lets you
list all the things, add or remove a thing, and reorder things, but it
doesn't help you order them, for example by saying "this one should go
after the one that has such-and-such set to so-and-so." Perhaps
NETCONF will save everything? I've been reading that Ansible is
ramping up support for it. But it's awful!

In the meantime, I've been using BSD more, and I sort of want it on my
router, if it's so much better designed or has a much nicer packet
filter or something. But BSD on routers seems to be sort of an x86
thing, like you get a desktop computer, put multiple network cards in
it, and voila; or you get a PCEngines board. It seems NetBSD won't run
on my MIPS-based router (specifically) while FreeBSD will (!?), and
FreeBSD for my router has nothing like the customization OpenWRT/LEDE
has, where entire subsystems of a usual desktop/server OS have been
removed and replaced with smaller, more purpose-built ones (glibc,
systemd, dbus, NetworkManager, firewalld, ISC dhcpd, etc.). It looks
like NetBSD has a flash-specific filesystem (CHFS) for a while now,
and a way to statically link a whole bunch of binaries into a single
file and make the different subsumed commands runnable using
hardlinks. I have no idea of the relative merits of NPF vs. any of
FreeBSD's `three` packet filtering systems vs. iptables.

Somebodyoughta make a router OS out of a BSD, and stick 9P support in
it, and use Rust or Go or something for all the new hotness that gets
added.
