LEDE IPv6 odyssey
#################
:date: 2017-03-31 00:05
:author: jaredj
:category: Projects
:status: published

It seems after all that my LEDE upgrade didn't work flawlessly. I
suddenly lost all of my IPv6 addresses (except the link-local ones,
natch). I've just quelled this rebellion by disabling odhcpd and using
dnsmasq-full to serve stateless DHCPv6 (`Android does not support
stateful DHCPv6
<https://code.google.com/p/android/issues/detail?id=32621>`_).

Along the way I discovered dnsmasq's support for adding IPs looked up
from names to an ipset. You normally can't make a firewall rule that
applies to a given DNS domain rather than a subnet, but this lets you
do just that. For example, it could let me block attempts to get to
Netflix over IPv6, which is needful because if I succeed in talking to
Netflix over IPv6, rather than the video I paid for they provide only
a message accusing me of dodging region restrictions.

But now that I have a lead on how to fix it, it appears not to be
broken any longer...?
