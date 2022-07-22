personal container cloud 2
##########################
:date: 2017-02-07 19:58
:author: jaredj
:category: Home IT
:tags: security
:slug: personal-container-cloud-2
:status: published

I've learned a few things. First, a firewall misconfiguration was
partly to blame. Second, neither Alpine's nginx package, nor netcat as
found in Debian, appear to support IPv6. The dhcp daemon can be
written into a systemd unit; I haven't done it yet. DNS updates might
happen if I were to serve DHCPv6 from my dnsmasq instance; I haven't
tried it yet. And acbuild is easy and quick to start using.
