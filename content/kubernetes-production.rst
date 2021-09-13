The road to production with Kubernetes
######################################
:date: 2021-09-13 10:53
:author: jaredj
:category: Projects

Up to now my Hive/Cortex on Kubernetes work has been focused on
getting things to initially work. Now I need to pay some attention to
how to keep them working, and get them working again when they break.

Use case
--------

For actual use, so far, I have five VMs with CentOS, plugged
appropriately into my organization's infrastructure (authentication,
logging, backup...). On these I'm running k3s, MetalLB, Traefik, and
Longhorn.

Logging
-------

`Kubernetes logging design documentation
<https://kubernetes.io/docs/concepts/cluster-administration/logging/>`_.

Logs have been kept and forwarded on my nodes before I ever installed
Kubernetes. The simplest way to get container logs collected and
forwarded is using the design from the above documentation labelled
`node logging agent`. This just means configuring the existing system
logger to pick up the container logs and forward them, as it's already
doing for the OS logs.

I found `a template`_ rsyslog.conf.d snippet, modified it as
necessary, and contrived to put it in
``/etc/rsyslog.d/05_containers.conf`` on all my nodes. I filled in
values for the ``RSYSLOG_*`` variables at the bottom, but your values
will vary so I left them for you. Here is a copy of the linked
template in case of link rot::

    global(workDirectory="/var/lib/rsyslog")

    module(load="imfile" PollingInterval="10")
    input(type="imfile"
          file="/var/log/containers/*.log"
          tag="container-logs")

    template(name="ContainerLogs" type="list") {
        property(name="timestamp" dateFormat="rfc3339")
        constant(value=" ")
        property(name="$!metadata!filename" regex.type="ERE"
            regex.nomatchmode="FIELD"
            regex.expression="([a-zA-Z0-9_-]*)-"
            regex.submatch="1")
        constant(value=" ")
        property(name="msg" spifno1stsp="on")
        property(name="msg" droplastlf="on")
        constant(value="\n")
    }

    action(type="omfwd"
           template="ContainerLogs"
           Target="${RSYSLOG_TARGET}"
           Port="${RSYSLOG_PORT}"
           Protocol="${RSYSLOG_PROTOCOL}")

    #action(type="omfile" dirCreateMode="0700" fileCreateMode="0644"
    # file="/var/log/messages" template="ContainerLogs")

.. _`a template`:: https://github.com/kincl/kubernetes-logging-syslog/blob/master/rsyslog.conf.template

Patching
--------

In my organization we have patching practices. Part of patching is
rebooting. If you do rebooting right, and you did your deployment
right with Kubernetes, you can do a rolling restart of the cluster
with no service downtime.

I found a piece of software for doing restarting right:
https://github.com/weaveworks/kured. A `blog post`_ evinces that it
has been around and maintained for at least a year—quite an
accomplishment in the Kubernetes space, I'm sad to say.

``kured`` works just like it says on the tin, so I'm not going to say
anything more about it here.

.. _`blog post`:: https://www.weave.works/blog/one-year-kured-kubernetes-reboot-daemon

Monitoring
----------

https://github.com/kubernetes/node-problem-detector takes OS-level
events and makes them available at the cluster level: for example, if
your kernel has an out-of-memory event and kills a process,
``node-problem-detector`` sees the resulting kernel messages and sends
them to Kubernetes as events about the node, so that they can be
reacted to at the cluster level. It also provides a Prometheus
endpoint for monitoring and alerting in that fashion.

Speaking of Prometheus,
https://github.com/cablespaghetti/k3s-monitoring has k3s-specific
installation and configuration directions for Prometheus and
Grafana. It does not go into making Prometheus and Grafana securely
available from outside the cluster. This method of setting up Grafana
does not involve persistent volumes, so changes you make in the
Grafana web UI will not persist. Instead you add custom resource
objects to your cluster to describe your dashboards.

I put all these Kubernetes objects in their own namespace,
``monitoring``.

Traefik
.......

Traefik is the example given in the k3s-monitoring repository: you add
a ServiceMonitor custom resource to tell Prometheus to scrape
Traefik's monitoring endpoint (I may have had to add this in other
namespaces too; can't quite remember); a PrometheusRule that defines
alert levels; and a ConfigMap that provides the dashboard to
Grafana. The Prometheus Operator takes care of turning those into
actual configuration for Prometheus, the alert monitor, and Grafana. I
didn't watch the Operator logs while changing things; my experience
was that I didn't have to restart things myself, but it took a couple
of minutes for the operator to do it—just long enough for me to hit
Refresh several times and wonder if it was working right.

Longhorn
........

Longhorn has an entire `set of directions`_ for Prometheus and Grafana
setup, which I skipped entirely. I think the ``k3s-monitoring`` stuff
got me most of this, and with operators and Helm charts instead of
manually added Kubernetes objects.

.. _`set of directions`:: https://longhorn.io/docs/1.2.0/monitoring/prometheus-and-grafana-setup

First, to get Prometheus to monitor ("scrape") Longhorn, I added this
resource to the cluster::

    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
      labels:
        app: longhorn
        name: longhorn-prometheus-servicemonitor
        release: prometheus
      name: longhorn-prometheus-servicemonitor
      namspace: monitoring
    spec:
      endpoints:
        - port: manager
      namespaceSelector:
        matchNames:
          - longhorn-system
      selector:
        matchLabels:
          app: longhorn-manager

Adding Grafana dashboards
.........................

There is a `Grafana dashboard`_ for Longhorn which I picked up and
installed. This is not explained in exact detail by the existing
sources, so I'm going to go into it here.

.. _`Grafana dashboard`:: https://grafana.com/grafana/dashboards/13032

When you download the dashboard JSON, the `export/import`_
documentation says that the JSON has an ``__inputs`` part that defines
some variables used throughout the rest of the JSON. When you import
the dashboard, values for these inputs are set. But the means of
providing dashboards to Grafana using Kubernetes resources doesn't use
Grafana's import mechanism, so you have to fix this up manually.

.. _`export/import`:: https://grafana.com/docs/reference/export_import/

The `JSON I downloaded`_ starts like this::

    {
      "__inputs": [
        {
          "name": "DS_PROMETHEUS",
          "label": "prometheus",
          "description": "",
          "type": "datasource",
          "pluginId": "prometheus",
          "pluginName": "Prometheus"
        }
      ],
      ...

.. _`JSON I downloaded`:: https://grafana.com/api/dashboards/13032/revisions/6/download

 And later on there are lots of parts like this::

        {
          "datasource": "${DS_PROMETHEUS}",
          ...
          "title": "Number Of Healthy Volumes",
          "type": "stat"
        },

So what I had to do was to remove the entire `__inputs__` object, and
find all the variable references ``${DS_PROMETHEUS}``, and replace
them with just "Prometheus," like ::

          "datasource": "Prometheus",

To find that value, I looked into other dashboards that were already
working in my Grafana instance.

Now to make it into a Kubernetes resource, I had to write a file like
this; let's call it ``longhorn-dashboard.yaml``::

     apiVersion: v1
     kind: ConfigMap
     metadata:
       namespace: monitoring
       name: longhorn-dashboard
       labels:
         grafana_dashboard: "true"
     data:
       longhorn-dashboard.json: |-
         {
           "__requires": [
              ...

 That is to say, I placed the entire Longhorn dashboard JSON file,
 with ``__inputs`` variable references fixed up and ``__inputs``
 removed, indented under ``longhorn-dashboard.json`` with the ``|-``
 thingy... *[refers to YAML spec]* um, that's a `block scalar`_ with a
 `strip chomping indicator`_.

 .. _`block scalar`:: https://yaml.org/spec/1.2.1/#id2793652
 .. _`strip chomping indicator`:: https://yaml.org/spec/1.2.1/#id2794534

From there, the operator takes that and stuffs it into Grafana's
configuration. I don't know how, and I don't have to yet.

More to come
------------

I'm going to touch on backup, hardening, reconstitution,
documentation, and resource reservation later.
