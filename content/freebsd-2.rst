FreeBSD for virtualization
##########################
:date: 2018-01-27 20:24
:author: jaredj
:category: Projects
:slug: freebsd-2
:status: published

I'm presently running an assortment of virtual machines on my desktop
using Fedora, KVM, and libvirt. I did this because I wanted one of my
virtual machines to have real video cards, and Fedora had a new enough
kernel at the time to just barely be able to do this. Over the past
couple of years it has added the capability of not crashing every time
I try to shut it down.

Meanwhile I've been listening to the BSD Now podcast, where they have
(unsurprisingly) many good things to say about FreeBSD, and ZFS in
particular. So I've kept trying different physical OSes. This time it
was FreeBSD as a Xen dom0. First I learned that my Athlon FX-8320E
can't run Xen PVH domains. Then I learned `what PVH is
<https://wiki.xen.org/wiki/Virtualization_Spectrum>`_, that dom0 can
be either PV or PVH, and then that FreeBSD 11 dropped PV dom0
support. So, no FreeBSD+Xen on this machine.
