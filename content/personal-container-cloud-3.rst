personal container cloud 3
##########################
:date: 2017-03-19 00:39
:author: jaredj
:category: Home IT
:tags: security
:slug: personal-container-cloud-3
:status: published

I decided I needed to use DHCPv6 to get the IPv6 address for my
container, so that if dnsmasq served the address it could update its
DNS (one nice thing it does), and I could at least get to my container
using a DNS name inside my own network, if not from elsewhere.

I updated my router from OpenWRT 15.05.1 to LEDE 17.01.0 (which worked
flawlessly), and then found that the default dnsmasq doesn't have
DHCPv6 compiled in, and then found that the UCI config file
`/etc/config/dhcp` doesn't feed dnsmasq DHCPv6-related things because
it expects to use odhcpd for that instead. I could likely make my own
dnsmasq.conf. Meh.

But that's OK, because I found out that the CNI dhcp helper-thingy
wasn't doing squat about IPv6, and won't until `this issue
<https://github.com/containernetworking/cni/issues/245>`_ is
fixed—which has had months of inactivity, but renewed discussion this
week. So the only reason my container had an IPv6 address was because
I had SLAAC enabled on my router, and the IPv6 stack just did the
right thing without being told anything. That's great but if nothing
else knows that address, I can't get to whatever the container will
serve without looking manually for that address, which will be newly
random every time the container starts.
