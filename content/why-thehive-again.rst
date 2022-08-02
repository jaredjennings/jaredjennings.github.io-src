Why TheHive again?
##################
:date: 2022-08-01 22:40
:author: jaredj
:category: Security
:tags: thehive, commentary

If I don't write down this doubt, it will continue to keep me from
proceeding.

TheHive (4) helps blue (defensive security) teams do their job. It
provides generalized, non-tool-specific alerts, with observables,
which can be promoted to cases. Cases are created from case templates
and have tasks which can be assigned to people, added, deleted, and
commented on with rich text. Observables can be sent for automated
analysis (e.g. VirusTotal can be searched for a SHA256 value) or
response (e.g. an IP can be sent to a responder which will tell a
firewall to block it). Tasks and cases can be closed. Everything can
be done not only via a real-time web interface, but also with APIs and
webhooks. Observables which have been seen before are automatically
flagged as such. Metrics are kept about cases and observables and can
be reported upon. Decent documentation is kept.

These are the features of TheHive which I've touched myself.

TheHive 4 also supports multiple organizations, where cases can be
shared between them or not. Multiple instances of Cortex, its analysis
engine, can be deployed and used, perhaps residing within different
security contexts.

Cortex also supports multiple organizations. Cortex performs analysis
and response using analyzers and responders, many of which have been
contributed by the community. These can be written in Python. It can
run them as subprocesses, inside Docker containers (given that Cortex
has insecure access to the Docker daemon), or using Kubernetes Jobs
(using code from a pull request that was never accepted).

TheHive is built for useful integration with MISP, an integration I
haven't explored. MISP has some concepts that TheHive appears to
duplicate, but MISP appears to be focused on automatic response to
shared threat intelligence, where TheHive is focussed on helping
people track manual tasks.

TheHive and Cortex are written in Scala using the Akka actor framework
and the Play web framework. TheHive (at production scale) requires an
Elasticsearch instance, a Cassandra database, and an attachment
store. Cortex requires an Elasticsearch instance. In production, both
should use OpenID Connect authentication. (TheHive 5 doesn't do
enterprise authentication unless you pay for it.)

This software might be minimal (I can't tell), but it is not
simple. If you want to run it in production, you need two kinds of
cloud databases, at least two kinds of file stores, and a private PKI
or two. You need to do monitoring, log collection, and backup. I can
see how Kubernetes can make some of these things easier to set up and
maintain---or make them someone else's job. I can see how it might be
possible to make a VM that starts out as a single machine running
TheHive and Cortex, and lets you scale out when you grow. I can
imagine that the scaling might be subjected to automated testing, so
it won't bitrot as components are upgraded.

But all that is a lot of work, and it's completely outside improving
the software itself. I don't know if any of it matters to anyone who
isn't already paying StrangeBee. And while I can imagine a way to
scale, a way to automate, and a way to test, I can't be sure that
every little underlying tech-stack decision is not going to splinter a
userbase that may be very small already.

I wrote an invitation to join me in forking TheHive 4, but I haven't
shared that invitation in the one place it matters the most: the Hive
Discord.
