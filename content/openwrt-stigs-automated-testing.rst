Somebodyoughta: OpenWRT + STIGs + automated testing
###################################################
:date: 2014-10-10 05:06
:author: jaredj
:category: Compliance at home
:tags: security, somebodyoughta
:slug: openwrt-stigs-automated-testing
:status: published

Both a `Firewall
STIG <http://securityrules.info/about/xonib-cusyz-kyfek-gitox>`__ and a
`Firewall
SRG <http://securityrules.info/about/xumac-cabon-pilup-digax>`__ exist.
They require things like `authentication for console
access <http://securityrules.info/about/xonib-cusyz-kyfek-gitox/SV-4582r3_rule>`__
and `suppressing router advertisements on external-facing IPv6
interfaces <http://securityrules.info/about/xumac-cabon-pilup-digax/SRG-NET-000019-FW-000191_rule>`__.

Assuming I want my home router and network materially to comply with
these documents, I could go through them, manually configuring the
router as I go. But then I could have made a mistake, or I could buy a
new router and have to do it all again. And all my effort would be
useless to anyone whose functional requirements and hardware aren't
exactly the same as mine.

I think OpenWRT already fulfills a good number of these sorts of
requirements out of the box. Perhaps it could be improved to do more of
them by default. Some others are up to how OpenWRT is configured. And
some of these requirements have more to do with the topology of the
network than the configuration of a single piece of it. I want to be
able to write exactly what changes are necessary to comply with each
security requirement, and I want to be able to test that those changes
do indeed fulfill the requirement.

In the desktop and server world, OVAL content fills the gap between the
kind-of-high-level requirements in an XCCDF checklist and the state of
the system: "to find out whether the minimum password length is long
enough, remember this number: 15; read the file /etc/foo/bar; look for a
line that matches the regex /minimum\_pass/; get the second word; parse
it as an integer; compare it to that number 15." Or something like that.
You run a tool like `OpenSCAP <http://www.open-scap.org/>`__ or maybe
Retina, which takes the XCCDF checklist and some OVAL definition files,
and evaluates the compliance of the system with the configuration
checklist. But OpenWRT runs on constrained enough platforms that it may
not be practical to check compliance in place: the binaries and check
content may not fit on the device, and the processing power may be
constrained enough that compliance checking interferes with normal
operation. What's needed, it seems, is a way to figure out what makes
for compliance and test it somewhere else, then reliably put that
configuration in place on the real device to obtain the compliant
behavior in production.

I've read recently about
`Beaker <https://github.com/puppetlabs/beaker>`__, which—if I've got
things straight—brings up a virtual machine with a given OS, installs a
given version of Puppet and Facter, runs a given Puppet manifest, and
then lets you make assertions about the final state of the system. It
helps Puppet Labs test Puppet, and also helps Puppet module authors test
their modules. It brings the OS into the test loop. Now, it seems
OpenWRT has an `x86 build
target <http://downloads.openwrt.org/barrier_breaker/14.07/x86/>`__, so
that you can easily virtualize it. And
`Vagrant <http://vagrantup.com/>`__ can bring up a
`multi-machine <http://docs.vagrantup.com/v2/multi-machine/index.html>`__
environment.

So, here's what *somebodyoughta* do: Make a tool that takes a
description of a `network
topology <https://www.google.com/search?q=dmz+topology>`__, in terms
suitable tersely to direct a person to set up a physical network of that
topology, and makes a Vagrantfile that sets up VMs and virtual networks
in that topology. Make something like `Puppet for
OpenWRT <https://github.com/solarkennedy/puppet-on-openwrt>`__ (that
project says, "Status: Dead") that can configure OpenWRT in a given way.
(`UCI <http://wiki.openwrt.org/doc/uci>`__ probably gets you more than
halfway there, but the tool may also need to install packages from opkg
and make extra config files outside of UCI. The tool should be able to
modify the configuration, not just overwrite it.) Make some test
description language that works across machines, with which you can say
something like, "To test the requirement that `the router must drop IPv6
packets with undefined header
extensions <http://securityrules.info/about/xumac-cabon-pilup-digax/SRG-NET-000019-FW-000194_rule>`__,
for each pair of interfaces A,B on the router, send a packet like such
into interface A. No packet should come out of interface B. This test
fully tests the requirement." If the test description language is
open-ended enough, like say it pokes commands to VMs using
`MCollective <http://puppetlabs.com/mcollective>`__ or
`Fabric <http://www.fabfile.org/>`__ or something, then you could write
a checklist with items like, "OpenWRT is not vulnerable to
CVE-YYYY-NNNN," and the test could be to run Metasploit with
such-and-such parameters on a virtual machine connected to the virtual
router.

With these tools in hand, you could easily test whether any changes made
to OpenWRT fulfill security requirements, you could easily convey how to
set up a network environment with certain compliance guarantees, and you
could test a given runtime configuration of OpenWRT against any kind of
requirements (security or functional).
