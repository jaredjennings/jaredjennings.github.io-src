personal container cloud
########################
:date: 2017-01-25 00:16
:author: jaredj
:category: Projects
:tags: security
:slug: personal-container-cloud
:status: published

Containers are real neat. I like how you can build a single thing that
contains a hunk of an application, and deploy both the initial version
and follow-on updates quickly. Containers are very easy to deploy to
any of a panoply of public clouds, but I want to host web apps for my
own use, containing my own data, on my own hardware.

And my hardware is a single box having an Athlon FX with eight cores,
8GB of RAM, and a couple of terabytes of mirrored spinning disks.

I've had my eye on OpenShift for a while now. It's a thing that can
build your code into containers, deploy the containers in various
slicey-dicey ways, and manage your web apps, including setting up DNS
so people can go to https://yourapp-you.openshift.example.com or some
such. I also looked at Deis, Rancher, and a couple of other whiz-bang
things. Besides a shocking loss of code diversity as everybody
scrambles to rebase everything on Kubernetes, what they have in common
is that the people who made them figure you must have at least three
beefy boxen to dedicate to your cloud, and more like a hundred, if you
are bothering to use their software. Oh, yes, try out our thing in a
Vagrant box, or run it as a container—but that's for developing,
debugging, kicking the tires; it might not remember things you told it
if you restart it.

Meanwhile, it seems that since I last checked, Docker has grown into
several products, rkt and appc have sprung up, and the Open Container
Initiative has begun (Gunnar and Dave let me in on that one). I'm
impressed with rkt and its attempts to be only one thing rather than
subsuming the world. In particular, I'm swayed by the case for using
systemd to manage containers rather than Docker's daemon. Perhaps,
like the time when PulseAudio stopped stuttering and started working,
this is systemd's moment to come into its own.

But everyone is building all their container networks on IPv4. How
silly! IPv6 is made for this sort of thing. I've only got one public
IPv4 address and it's dynamic. And what if I want to have fun with
containers that live on a darknet instead?

So here's what I've got so far on how to have fun running containers
on a single box.

 1. Make a VM and install CoreOS Container Linux. (I got version
    1248.4.0.) This entails getting the iso, constructing a cloud-config
    file, making that into an iso, mounting it on the VM, and running
    coreos-install with it. My cloud-config.yaml goes like::

      #cloud-config
      coreos:
        update:
          reboot-strategy: best-effort
      ssh_authorized_keys:
        - "ssh-rsa AAAA..."
      hostname: "myhostname"

 2. (coreos-install needs outbound https.) Once booted, the CoreOS box
    obtains an address on my fd00::/16 local network. Add a firewall
    rule to allow my internal box to ssh to it, and ssh
    core@myhostname. Find out the real 2001:db8::/48 IP, add another
    firewall rule for ssh, add a DNS entry.

 3. Read about `rkt networking
    <https://github.com/coreos/rkt/blob/6e3292bfa3d2d0238df3402ba9fe2f73327335f5/Documentation/networking/overview.md>`_
    using CNI plugins. Create ``/etc/rkt/net.d/10-dmz.conf`` with
    these contents::

      {
        "name": "dmz",
        "type": "macvlan",
        "master": "eth0",
        "ipam": {
          "type": "dhcp"
        }
      }

 4. Read about the dhcp plugin. Find
    ``/usr/lib/rkt/stage1-images/stage1-coreos.aci``. ``rkt fetch`` that sucker as per the `dhcp section <https://github.com/coreos/rkt/blob/6e3292bfa3d2d0238df3402ba9fe2f73327335f5/Documentation/networking/overview.md#dhcp>`_, then follow the rest of the directions.

 5. Run ``sudo ./dhcp daemon``. Ctrl-Z, bg.

 6. ``sudo rkt run --net=dmz --interactive
    quay.io/coreos/alpine-sh``. Inside the container, run ``ip a`` and
    see the unique IPv6 address.

 7. ``sudo rkt gc --grace-period=0s`` and watch the dhcp lease get
    released.

 8. Wonder how to ever remember where that silly ``/home/core/dhcp``
    executable came from; write silly manual directions.


Unanswered questions:

 * How can that dhcp thingy be made suitably repeatable or automatic?
   Why isn't that part of CoreOS?
 * How can the containers update a DNS server with their IPv6
   addresses?
 * `onionboat <https://nonconformity.net/2016/06/10/onionboat-using-docker-for-easy-tor-hidden-services/>`_
