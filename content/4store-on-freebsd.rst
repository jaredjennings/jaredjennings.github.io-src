building 4store on FreeBSD
##########################
:date: 2017-12-27 23:03
:author: jaredj
:category: Security
:slug: 4store-freebsd
:status: published

To build 4store on FreeBSD, of course you need Raptor, Redland and
Rasqal: pkg install redland. And the autotools: pkg install autoconf
automake libtool. Git to check it out: pkg install git. You need glib,
and libxml if you don't have it already. readline, for some
reason. And ossp-uuid, without which it will segfault for no
discernible reason. And you have to configure it with
``CFLAGS='-I/usr/local/include' LDFLAGS='-L/usr/local/lib'``.

I say this because there is no 4store port, and FreeBSD's shell
doesn't keep history across sessions, and FreeBSD's sudo doesn't log
what you do (!?).

I've already given up on putting this in a jail, after the fourth time
of running into https://github.com/iocage/iocage/issues/302 since
October, apparently because `stability
<https://forums.freebsd.org/threads/52843/>`_ is better than fixing
bugs.
