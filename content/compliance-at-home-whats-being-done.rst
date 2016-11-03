Compliance at home: What's being done
#####################################
:date: 2014-03-07 05:47
:author: jaredj
:category: Compliance at home, Projects, Security
:tags: nist, oval, scap, security, standards, xccdf
:slug: compliance-at-home-whats-being-done
:status: published

Last time I talked about the documents I've seen and used that contain
security requirements at various levels of detail, and I said I'd speak
more on what's being done to automate compliance, and what should be
done instead.

What's being done is `SCAP <http://scap.nist.gov/>`__. This is a
specification that binds together a bunch of other standards, namely
XCCDF, OVAL, OCIL, and CVE and friends. Some part of the idea is that
some person or
`community <https://fedorahosted.org/scap-security-guide/>`__ makes a
STIG using the XCCDF format. Someone makes OVAL that describes how to
check for and possibly change system configuration; then a tool reads
both XML files, uses the OVAL to find out how the system is configured,
checks it against how the XCCDF says the system should be configured,
and either renders a report of how compliant the system is, or, if the
OVAL writer wrote enough OVAL, fixes the system. (Missing from my
description: how OCIL, CPE, CCE, CVE, CVSS, CCSS and XML signatures play
in.)

The problem with this is that it's focused solely on security. That
means a security-specific tool needs to know how to change the
configuration of my system in general, so it's duplicating knowledge
that is already kept and improved using languages like Puppet, Chef,
Salt, cfengine, and the like. It also means that if I need a complete
accounting of all the configuration changes being made to my system for
any reason, I can't look in just one place. It means two tools can fight
over how the system should be configured. It means two infrastructures
for control and reporting talking across my network. As an admin at
work, I don't want this headache. As an admin at home, I have no time to
maintain it and it just won't get set up.

A few months ago, `Dave and Gunnar <http://dgshow.org/>`__ talked about
the origins of SELinux on their podcast, and they said a great thing
about SELinux was that it brought the trusted operating system kernel
into the mainstream, where previously it had been an expensive separate
product for a tiny side market. I think this is what should happen for
security-related system configuration as well, and I'll elaborate
further later.
