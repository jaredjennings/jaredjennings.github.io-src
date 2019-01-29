Rejecting NetBSD in early 2019
##############################
:date: 2019-01-29 00:40
:author: jaredj
:category: Projects

I've got this Dell Latitude E4300 laptop. The battery has stopped
working long ago, but the computer hasn't. I had FreeBSD on it, with
UFS, and maybe the power went out, or maybe I shut it down wrong, but
it ceased to be able to boot. So I put NetBSD on. Here is what I've
found and why I'm quitting using it. Note that these are things I
could have done something about. The first thing is to say what they
are though. And these are all pkgsrc, not NetBSD, issues.

The Firefox (64.0.2) in pkgsrc depends on libicui18n, and this library
got upgraded to a new major soversion 63, but Firefox wasn't built
against it, so suddenly after an upgrade my browser didn't work.

mozilla-rootcerts is a way to get the normal root certs trusted. Not a
very integrated way, but - it puts root certs under
/etc/openssl/certs, and has for some ten years, while dillo is
hardcoded to look under /etc/ssl. Dillo's code has a comment
suggesting they know they need to get better at finding the root
certs, more flexible, but they haven't.

OpenJDK is in pkgsrc; good. But Arduino is not. And when I try to
build it myself, the build works (once I get GNU tar to be the tar
used... I just made a symlink /usr/pkg/bin/tar pointing at
/usr/pkg/bin/gtar, and put /usr/pkg/bin at the front of PATH), but
running fails with some odd shared library error. (Note that I
casually dropped the term `soversion` above. It wanted four of
something but only had two. I've seen many shared library errors, but
never the likes of this one.)

NetBSD was capable of sending my laptop to sleep, but not waking it
again. Eh.

So that's why I'm quitting NetBSD at this time. Maybe I'll be back,
but you see I've just finished this 3-D printer and I have to build
its firmware (which has no Makefile so I have to use Arduino)
post-haste. Back to FreeBSD.
