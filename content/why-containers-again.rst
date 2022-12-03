Why containers, again?
######################
:date: 2022-07-22 22:25
:author: jaredj
:category: Security
:tags: thehive, cortex, kubernetes

I've seen some difficulties people have had building and installing
TheHive and Cortex just on their own, without Kubernetes. With some
people being less enamoured with Kubernetes these days, it's worth
remembering why I think adding this additional complexity is a good
idea.

 * It shifts work from being specific to these applications, toward
   being general cloud admin work.
 * For cloud deployments, a lot of Kubernetes' complexity is handled
   by other people.
 * For on-premises deployments, Kubernetes admin work is being
   minimized and automated, thanks to the trend of "edge computing,"
   by a lot of sharp people who aren't me.
 * The Kubernetes Operator pattern may help automate remaining
   application-specific maintenance and upgrade tasks.
 * Deploying with Kubernetes solves redundancy without doubling admin
   work, and solves scaling without multiplying admin work. (It adds a
   large constant value, but that's displaced toward development.)
 * The architectural decisions already made (Akka, Cassandra,
   Elasticsearch, S3 API) are harmonious with cloud deployment and
   scaling.
 * It seems easier this way to split out different concerns to
   different software that's better at solving those concerns, rather
   than having to integrate it into the application. Examples:
   authentication (e.g. with Keycloak), monitoring (Prometheus,
   Kubernetes; contrast MISP's built-in agent monitoring), and maybe
   even analytics and metrics (Grafana, although TheHive has some good
   metrics built in already).
 * The work it takes to make the application assume less about its
   environment may also pay off for other deployment methods--Nomad,
   systemd containers, FreeBSD jails or pots, or what-have-you.
