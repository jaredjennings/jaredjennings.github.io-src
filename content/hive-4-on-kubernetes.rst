Hive 4 on Kubernetes
####################
:date: 2021-03-10 15:59
:author: jaredj
:category: Security
:tags: kubernetes, helm, thehive, thehive4, k3s, longhorn

**UPDATE**: I made an unofficial Helm chart at
https://github.com/jaredjennings/helm-thehive. It does a lot of this,
but has no documentation yet. Soon.

Here's what I've got so far. It is not complete. For example, it has
no persistent file storage, and it isn't geared up for Cortex.

When you see YAML, to act on it, save it in a file and ``kubectl
apply -f thefile.yaml``.

First, install k3s per directions on k3s.io. Any Kubernetes will do,
but this one has Traefik by default, super simple setup, and runs both
on one node and multiple.

Install Longhorn per its directions.

.. code:: sh

    helm install -n thehive cassandra bitnami/cassandra --set persistence.storageClass=longhorn

Add a Play secret. (You may need to install pwgen, or just set pw to
something long and random instead of ``$(pwgen ...)``.)

.. code:: sh

    (set -x; pw=$(pwgen -s 24 -n 1); echo $pw; \
     kubectl create -n thehive secret generic hive-play-secret --from-literal="secret=$pw")

Create the service.

.. code:: yaml

    apiVersion: v1
    kind: Service
    metadata:
      name: thehive-web
      namespace: thehive
    spec:
      selector:
        app: thehive
      ports:
        - protocol: TCP
          port: 9000

Create the deployment.

.. code:: yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: thehive
      namespace: thehive
      labels:
        app: thehive
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: thehive
      template:
        metadata:
          labels:
            app: thehive
        spec:
          containers:
            - name: thehive
              image: 'thehiveproject/thehive4:latest'
              volumeMounts:
                - mountPath: /opt/data
                  name: data
              env:
                - name: TH_SECRET
                  valueFrom:
                    secretKeyRef:
                      name: hive-play-secret
                      key: secret
                - name: CQL_HOSTNAMES
                  value: cassandra
                - name: TH_NO_CONFIG_CORTEX
                  value: '1'
                - name: CQL_USERNAME
                  value: cassandra
                - name: CQL_PASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: cassandra
                      key: cassandra-password
          volumes:
            - name: data
              emptyDir: {}

This ingress object makes Traefik route requests for
``thehive.my.domain`` to TheHive's service.

.. code:: yaml

    apiVersion: extensions/v1beta1
    kind: Ingress
    metadata:
      name: thehive
      namespace: thehive
      annotations:
        kubernetes.io/ingress.class: traefik
    spec:
      rules:
        - host: thehive.my.domain
          http:
            paths:
              - backend:
                  serviceName: thehive-web
                  servicePort: 9000
                path: /

