FreeBSD jails and FIBs
######################
:date: 2023-02-04 14:56
:author: jaredj
:category: Home IT

History and constraints
-----------------------

In 2013, I decided I wanted home server workloads separated from my
desktop machine in a more proper DMZ. My QNAP filer had just died, and
I wanted to reduce space utilization, power, and heat. I set up
virtualization using libvirtd on Fedora, and managed to do GPU
passthrough using AMD cards. I used 802.1q VLANs from my router to my
PC, set up a bridge for each VLAN, and connected VMs to the
bridges. My filer became a VM. I got a hot-swap hard drive cage, moved
the filer's drives into the PC, and passed them through to the filer
VM, which ran Debian Stable and served NFSv4.

More recently, I tried to centralize storage better, so I'd have less
separate backups to keep track of. I set up a FreeBSD machine, with
ZFS. I wanted to store all the data from the DMZ on the same ZFS pool,
so (after much hand-wringing) I connected my FreeBSD box to both the
inside and DMZ networks, and served NFSv4 to them both. Then I moved
the VMs over to the FreeBSD box, and decided to turn them into
jails. This way I could dispense with NFS for them, and just mount the
data into the jail using nullfs: faster and simpler. Jail separation
is enforced by the kernel, not the CPU, but it's a post-Spectre and
Meltdown world. CPUs aren't as trustworthy as they used to seem, and
I'm running on old used equipment here. FreeBSD jails have been
hammered on in production for 25 years. I don't have the time to
administer as many OS instances as I used to, I'm not as scared of
targeted attacks as I used to be, and preventing attacks isn't
reckoned to be as great a proportion of the meaning of security as it
used to be.

Now, I spent some time setting things up with Kubernetes, and I really
liked the ingress idea, where a reverse proxy sits in front of your
services and is dynamically reconfigured as you add and remove
services to make them available. The FreeBSD folks don't have
everything hooked up to APIs like Kubernetes does, so it's much easier
with jails to statically configure IP addresses, and it's no harder to
statically configure the reverse proxy. Traefik is available, so I set
it up in a jail. The recommendation is to run it as some nonroot user,
which means it has to listen on high ports (1024 or greater), like
8888 or 8443. Then you NAT connections incoming to port 80 or 443, so
they go to the Traefik jail on the high ports. Works fine for IPv4,
and that's all anyone uses, right? I do tend to use IPv6, but I
couldn't get it working, and I had a Nextcloud to set up. So I just
satisfied myself with IPv4 for this purpose.

Fast-forward to now. I'm moving off of Traefik to Caddy, because it
has a slightly smaller memory footprint. Caddy tries to go get a TLS
certificate from LetsEncrypt; LetsEncrypt tries to connect to my Caddy
jail over IPv6; it doesn't work right, because the packet is coming in
on port 443, and it's not being NATted like it would under IPv4, so
there's no opportunity to magick that into a connection to port 8443.

I decided to run Caddy as root. It's used to dropping root after
binding to low ports - it's a web server first and a
web-everything-else-tool afterward, and it's maybe not as specifically
built for Linux containers like Traefik is. In a Linux container you
aren't supposed to do anything as root, because the isolation between
container root and host root is tenuous. But FreeBSD jails were
*originally intended* to be a way to constrain root. There are less
different kinds of interfaces to namespace (sysfs, proc, etc, etc),
and jails have been attacked, and patched, for longer.

The problem
-----------

After some iterating, I got the config whipped into shape, but I
couldn't get at Caddy. To my surprise, LetsEncrypt could, and my
wireless VLAN also could. But my inside wired VLAN couldn't. This jail
host, I might add, is not directly connected to the wireless VLAN nor
to the outside, only to the inside wired VLAN and the DMZ VLAN. So it
was clear enough that the problem had something to do with my jail
host being connected to both of these LANs. I can't disconnect from
either, because it stores things for the inside VLAN, and it runs
jails for the DMZ VLAN.

Troubleshooting
---------------

You can't tcpdump in a shared-IP jail, and you can't ping by
default. ``nc`` is better than nothing, but it wasn't really making
anything clearer. Running tcpdump on the DMZ VLAN on the jail host,
outside the jails, I could see SYN packets coming from inside
addresses, but nothing in return. Running tcpdump on the router, I
could see that the SYN packets were going through it. Running tcpdump
on pflog0, I didn't see any dropped packets being logged. Where were
they getting silently dropped?

I figured out that I had two underlying problems: `asymmetric
routing`_, and anti-spoofing. My jails were using the same routing
table as the host system. So when a jail with only a DMZ address
needed to send something to the internal network, that packet would be
sent out *over the inside interface*, with a DMZ source IP. Packets
from inside to this DMZ jail, however, would go through the router,
into the DMZ interface of the host, through the firewall, and into the
jail. This is *asymmetric routing*, and while I'm sure it could be
desirable under some carefully controlled circumstances, in general
it's to be avoided.

.. _`asymmetric routing`: https://www.jasonvanpatten.com/2015/12/29/freebsd-jails-filesystems-and-fibs/

And it would have worked, too, if it hadn't been for you meddling
antispoof rules! In my pf.conf, I had::

  antispoof in quick for { lo $int_if $dmz_if }

You always don't want spoofing, right? I overlooked it so many
times. But with packets still being dropped, I noticed this was the
only `quick` rule in my policy, and the only block without a log. I
looked up what `antispoof` means, and found (``pf.conf(5)``):

    The antispoof directive expands to a set of filter rules which
    will block all traffic with a source IP from the network(s)
    directly connected to the specified interface(s) from entering the
    system through any other interface.

    For example, the line ::

        antispoof for lo0

    expands to ::

        block drop in on ! lo0 inet from 127.0.0.1/8 to any
        block drop in on ! lo0 inet6 from ::1 to any

So antispoofing for my DMZ interface was causing ::

  block drop in on ! $dmz_if inet6 from $dmz_subnet to any

So my packets headed out the inside interface had a DMZ subnet source
address, but were ``on`` the internal interface, ``! $dmz_if``, and so
they were being dropped - quickly (without consulting the pass rules
below), and without logging.

The tool
--------

The solution is FIBs. This stands for Forwarding Information Base, and
it's a separate routing table. See ``setfib(2)``, and look for "fib"
in ``route(8)``. You can run a process under a separate FIB using
``setfib(1)``, sort of like chroot but for routing tables instead of
the filesystem. You can tell ``iocage`` to use a different FIB for a
jail by setting the jail's ``exec_fib`` property.

Wielding the tool
-----------------

That's the tool, but what's the policy? Specifically, my jails that
are on the DMZ should not know that there is a route out of this
machine via the interface connected to the inside VLAN. They'll have
to send their packets for inside to the router - which is how it
should be anyway, because going between LANs should necessitate going
through the firewall on the router.

So first I set ``net.fibs=2`` in ``/boot/loader.conf`` and reboot. Now
FIB 0 is my default FIB, where everything happens unless I say
otherwise. And here are the routes I had to add to FIB 1:

 * ``-net`` my DMZ IPv4 subnet ``-iface vldmz``.
 * For each DMZ jail, ``-host`` the jail's IPv4 address ``-iface
   lo0``: DMZ jails can talk to each other over the loopback
   interface. Caddy wouldn't start because it couldn't talk to its own
   IP address till I had this in.
 * For each DMZ IPv6 subnet, similarly, ``-net`` the subnet ``-iface
   vldmz``. (I have an fd00::/8 ULA subnet for traffic local to my
   home, and a routable subnet.)
 * For each DMZ jail, ``-host`` the jail's IPv6 address ``-iface
   lo0``.
 * ``-net fe80::%vldmz/64 -iface vldmz``: DMZ-link-local traffic can
   happen over the vldmz interface.

All this info will come in real handy when I reboot the jail host,
because I haven't configured anything to run at boot time to put these
routes in place yet. :)

EDITED TO ADD:

Fancy boot script
-----------------

(Real IP addresses replaced with examples.) ::
    #!/bin/sh
    # https://savagedlight.me/2014/03/07/freebsd-jail-host-with-multiple-local-networks/
    # https://www.jasonvanpatten.com/2015/12/29/freebsd-jails-filesystems-and-fibs/
    # https://j.agrue.info/freebsd-jails-and-fibs.html

    . /etc/rc.conf
    . /etc/rc.subr

    #route="echo route"
    route="route"

    # FIB 1 is used for DMZ jails. Some of them talk to each other (e.g.,
    # a web app jail talks to a database jail). They need to do this over
    # the loopback interface. So there needs to be a route in FIB 1 for
    # each IP address of each DMZ jail, saying to use the interface lo0.

    # we are going to call iocage a lot. if it is off, avoid this.
    if checkyesno iocage_enable; then
      echo "rc.local adding per-jail local routes"
      for fib_number in 1; do
        # hmm, you know, i should skip this for vnet jails
        for jailname in $(iocage get -H -r exec_fib | awk "\$2==${fib_number} { print \$1 }"); do
          # for each ip6_addr in e.g. vldmz|2001:db8:.../64,vldmz|fdff:db8:.../64
          ip6av=$(iocage get -H ip6_addr $jailname)
          if [ "$ip6av" != "none" ]; then
            for ip6_addr in $(echo $ip6av | tr ',' '\n' | sed 's/^.*|//; s,/[0-9]*$,,'); do
              $route -6 add -host $ip6_addr -iface lo0 -fib $fib_number
            done
          fi
          # similarly with ip4_addr e.g. vldmz|192.0.2.4/24,vldmz|192.0.2.2/24
          ip4av=$(iocage get -H ip4_addr $jailname)
          if [ "$ip4av" != "none" ]; then
            for ip4_addr in $(echo $ip4av | tr ',' '\n' | sed 's/^.*|//; s,/[0-9]*$,,'); do
              $route add -host $ip4_addr -iface lo0 -fib $fib_number
            done
          fi
        done
      done
    else
      echo "rc.local not adding per-jail local routes: iocage_enabled is off"
    fi

    $route -6 add -net fdff:db8::/64 -iface vldmz -fib 1
    $route -6 add -net 2001:db8::/64 -iface vldmz -fib 1
    $route -6 add -net fe80::%vldmz/64 -iface vldmz -fib 1
    $route add -net 192.0.2.0/24 -iface vldmz -fib 1

    $route -6 add default fdff:db8::1 -fib 1
    $route -6 add default 2001:db8::1 -fib 1
    $route add default 192.0.2.1 -fib 1
