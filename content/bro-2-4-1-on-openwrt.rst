Bro 2.4.1 on OpenWRT
####################
:date: 2016-04-07 02:21
:author: jaredj
:category: Security
:tags: security
:slug: bro-2-4-1-on-openwrt
:status: published

.

    "Holy waffles if troubleshooting build errors in a large Autotools
    mess isn’t the most hemorrhage-inducing activity known to mankind."

    .. raw:: html

       <footer>

    —\ `krkhan <http://inspirated.com/2015/06/08/release-bro-2-3-1-2-on-openwrt>`__\ 

    .. raw:: html

       </footer>

I've taken krkhan's
`packaging <https://github.com/krkhan/openwrt-bro>`__ of
`Bro <https://www.bro.org/>`__ 2.3.1 for
`OpenWRT <https://openwrt.org/>`__, and `updated
it <https://github.com/jaredjennings/openwrt-bro/tree/update-to-2.4.1>`__
to package Bro 2.4.1 on the present OpenWRT trunk. This was necessary
because 2.3.1 is no longer available for download.—Except, you know, in
the
`archive <https://www.bro.org/downloads/archive/bro-2.3.1.tar.gz>`__.
Whatever. It's not the newest version anymore, and it is
security-related, and it has a ton of protocol analyzers in it, in which
vulnerabilities `like
these <https://web.nvd.nist.gov/view/vuln/search-results?adv_search=true&cves=on&cpe_vendor=cpe%3a%2f%3awireshark&cpe_product=cpe%3a%2f%3awireshark%3awireshark&cvss_version=3&cve_id=>`__
might be found, so one should keep it updated.

It builds; I don't know if it works yet. But I've never run Bro before,
so problems might take a bit to flush out. I'm going to eat the ice
cream of victory now.

Here's what I know about Bro: it is a language and runtime system for
expressing and handling events that happen on a network. The events may
be very basic ("a packet was seen with protocol TCP and destination port
123") or more refined ("within a telnet connection, these keystrokes
were sent just after the text 'Password:' was received," or so). So it
started life being called an intrusion detection system, but has gained
much more general significance. I think this is how it is different from
Snort and the like. Bro has a nice `hands-on
tutorial <http://try.bro.org>`__, which I'm going through now.

The reason it is exciting to have Bro on OpenWRT is that it should make
some modern security capabilities deployable to a home network. With a
compliance focus, I can look at all the guidance that some people think
is a good idea, decide how much of it makes sense for me, and then try
to figure out how to implement and track that compliance at a small
scale. I'm personally motivated, because I've thought through the ways
one could break in without that compliance in place. This is likely
analogous to reading news stories about a burglary, reading up on
locksmithing, and buying a better front door lock, because the usual
locks have design deficiencies: It's probably an improvement, but
narrowly focused and possibly irrelevant. But anyone could benefit from
knowing the usual sorts of connections made, and knowing when weird
things seem to be afoot. People are even starting to try to sell
services like this, mediated by routers whose firmware they control. But
of course I think people should be in control of their own computing
equipment, no less than companies are.

A bit on what I actually did: Bro 2.3.1 required five patches to build
properly under OpenWRT, and krkhan generated those patches. I updated to
Bro 2.4.1, and most of those patches didn't apply cleanly anymore. So I
was able to find that one isn't necessary anymore, and regenerate
another one. Then there was some source code that doesn't compile under
the compiler presently used in OpenWRT trunk, i.e. gcc 5.3.1. Fixed
that. Then, I found that the musl C library is being used, which is
great, it's smaller, but it doesn't have the ``fts`` API, which is used
for iterating over files and directories (like ``os.walk`` in Python). I
found `musl-fts <https://github.com/pullmoll/musl-fts>`__ (thanks!)
which implements that API, packaged it, and made Bro build against it.

You'll likely find out whether it works first here.
