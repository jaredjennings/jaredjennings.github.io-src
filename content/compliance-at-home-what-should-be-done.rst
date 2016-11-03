Compliance at home: What should be done
#######################################
:date: 2014-03-09 02:56
:author: jaredj
:category: Compliance at home, Projects, Security
:tags: chef, disa, nist, puppet, security, standards
:slug: compliance-at-home-what-should-be-done
:status: published

Last time I shared my doubts about the applicability of the way security
configuration is being done to home administrators. So what do I think
we should all be doing instead of what NIST and DISA think we should be
doing?

These things: Describe security-related system configuration changes
using languages and tools that already exist for describing general
system configuration changes. Submit patches to code others have already
written in these languages, to make generic code fulfill specific
security requirements. Use some novel method to document which security
requirements are fulfilled, so that interested people can collect these
assertions.

For example, someone has written some code in Chef that configures an
Apache web server, blissfully unaware of the security needs of various
large organizations. Instead of coding up a bunch of unrelated XML to be
consumed by a separate tool that will fight with Chef, submit patches to
the Chef Apache recipe maintainer that make the recipe capable of
configuring Apache to be secure in the prescribed ways.

There are two main differences between this and what I understand of
SCAP: one, it involves more people and more code from outside
security-specific circles; and, because of this, two, assertions that
the code brings a system into compliance with a security requirement are
to be tested and not taken on trust.
