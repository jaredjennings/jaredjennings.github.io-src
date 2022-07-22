Somebodyoughta: Plan9 + routing
###############################
:date: 2015-01-26 06:09
:author: jaredj
:category: Home IT
:tags: somebodyoughta
:slug: somebodyoughta-plan9-routing
:status: published

I've worked a lot with OpenWRT lately, making it do things I've never
made it do before, like provide IPv6 prefixes to downstream routers,
consume IPv6 prefixes from upstream routers, block all traffic by
default, and provide real, not-local-only IPv6 addresses to a management
network without promising to route traffic from that network anywhere
else. It's comforting to use traditional Linux tools like ``vi``, ``ip``
and ``less`` to manage the router, but I feel nervous because none of my
changes were tracked, so I have no way to know when I made a change or
why. While `UCI <http://wiki.openwrt.org/doc/techref/uci>`__ promises to
provide the seeds of scriptable remote configurability, not all the
changes I made were to files that UCI controls. And busybox lacks a few
things I use all the time, like searching for a string from ``less``, or
macros in ``vi``. Whatever UCI controls, it does well, but the rest is
shell scripts, which bind other programs together easily enough, but are
difficult to edit programmatically.

So I was thinking as long as you're going to have a limited shell, why
not make it ``rc`` from Plan 9, and ``cpu`` in instead of ``ssh``. That
way you get scrolly windows for free when you use ``drawterm`` or a Plan
9 terminal window. The problem with this is that ``rc`` isn't nearly so
nice if you can't get to everything as a file: any part of the design of
Plan 9 requires the rest. But the more Plan 9 design you pull in, the
more you discard from established codebases like ``ntpd``, ``iproute``,
and, in the limit, the Linux kernel.

Really what I want is a simpler, more orthogonal interface for
configuration of the same proven codebases that millions of others use
and hundreds of others make secure. (Rewind a few years, remix, and I
could have been one of those folks harping about using XML for every
config file. Oops.) UCI was a big effort, its code is nearly as small as
libixp, and it's working software and not just an idea. I should build
on it. Well—somebodyoughta, anyway.
