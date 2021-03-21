Cortex on Kubernetes
####################
:date: 2021-03-09 14:15
:author: jaredj
:category: Projects

**UPDATE**: Cortex Helm chart created. See details below.

Cortex is a piece of software for cybersecurity professionals, which
coordinates analysis of observables found during investigations, and
automated response to the findings of the analyses. For example,
suppose a user receives a phishing email. The "From" address is an
*observable*; one way to analyze it would be to find out who else
within the organization got an email from that address
recently. Perhaps the email contains a web link; analysis could find
that it leads to an unsafe site, and one way to respond might be to
tell the organization's web proxy to block that page.

Cortex (I'm writing about version 3.1.0) supports different ways to
run those *analyzers* and *responders*.

One way is that Cortex creates input files on a filesystem, and spawns
a subprocess. The subprocess writes output files, then exits. Cortex
reads the output and formulates the report. This is simple, and could
perhaps be secured tightly using SELinux or AppArmor; but it requires
the code of every analyzer and responder, plus any libraries they
need, to be installed within the same filesystem namespace as Cortex,
even though development of analyzers and responders need not follow
the same rhythm, nor even be done by the same people, as Cortex.

Another supported way to run analyzers and responders is using
Docker. Cortex is run inside a Docker container; it's handed a volume
pointing at a directory on the host for job I/O, and it's handed the
host's Docker socket. Then, to run an analyzer or responder, Cortex
writes the input files, and asks Docker to spawn a new container, with
the job I/O directory as a volume. The image run is specific to the
analyzer/responder, and contains only that code and its
dependencies. Now the analyzers and responders can be built and
packaged separately, each in their own proper time. If they require
different versions of dependencies, this is no problem. But handing
the Docker socket into a container is not recommended from a security
point of view: it is the same as root access to the machine. The
Docker socket will only allow running containers on the same machine,
which impairs scalability. And this also makes Cortex depend
specifically on Docker, at a time when other software that deals with
containers is flourishing with many new ideas.

Building on the excellent work done in making the job runner an
extension point of Cortex, I filed a `ticket`_ to request a Kubernetes
job runner, and then a `pull request`_ with an implementation of it.

.. _ticket: https://github.com/TheHive-Project/Cortex/issues/347
.. _`pull request`: https://github.com/TheHive-Project/Cortex/pull/349

**UPDATE**: https://github.com/jaredjennings/helm-cortex is a Helm
chart embodying all I've learned
below. https://hub.docker.com/r/jaredjennings/cortex is a build of the
code I've submitted in the pull request. It only has a `latest` tag,
and Helm doesn't let you override the appVersion, so my chart
presently says the appVersion is "latest." This is frowned upon,
because Helm charts are supposed to do the same thing a week from now
that they did today, and "latest" can certainly change from now to
then. Take it as an indication of the relative immaturity and
instability of all this stuff that my chart uses the "latest"
appVersion, and the chart itself has a 0.x version number.

One of the goals I set out in the ticket was some kind of
documentation about how to make it work. Here's how I did that at
home. Perhaps it may form the germ of some documentation appropriate
for Cortex users in general.

Where you see YAML source below, the way to act on it is to write it
into a file and `kubectl apply -f thefile.yaml`.

1 K8S setup
-----------

1.1 DNS names
~~~~~~~~~~~~~

On my home router, in /etc/dnsmasq.conf:

.. code:: sh

    # Entire k subdomain goes to kubernetes node
    address=/k.my.domain/192.168.x.y

1.2 k3s
~~~~~~~

Set up as directed at k3s.io. Default Traefik ingress included.

1.3 helm
~~~~~~~~

Set up as directed at helm.sh.

1.3.1 Helm repos
^^^^^^^^^^^^^^^^

.. table::

    +---------+----------------------------------------------------------------------------+------------------------+
    | NAME    | URL                                                                        | FOR                    |
    +---------+----------------------------------------------------------------------------+------------------------+
    | bitnami | `https://charts.bitnami.com/bitnami <https://charts.bitnami.com/bitnami>`_ | usual stuff like mysql |
    +---------+----------------------------------------------------------------------------+------------------------+
    | twuni   | `https://helm.twun.io <https://helm.twun.io>`_                             | docker-registry        |
    +---------+----------------------------------------------------------------------------+------------------------+

2 insecure local unauthenticated registry
-----------------------------------------

Traffic to registries is https by default. hub.docker.com, which many
consider to be a default registry, recently implemented usage caps for
free users. I didn't want to run into that. I also didn't want to
bother with https for my local registry. *Don't do this in production*!

2.1 install
~~~~~~~~~~~

.. code:: sh

    helm install registry twuni/docker-registry --set ingress.enabled=true,ingress.hosts\[0\]=registry.k.my.domain

2.2 use
~~~~~~~

for pushing, in /etc/docker/daemon.json:

.. code:: json

    { "insecure-registries":["registry.k.my.domain"] }

for pulling, in /etc/rancher/k3s/registries.yaml:

.. code:: yaml

    mirrors:
      "registry.k.my.domain":
          endpoint:
            - "http://registry.k.my.domain:80"


3 building Cortex inside Docker
-------------------------------

I never quite managed to get the right environment for building
Cortex, and about the second or third try, I stopped wanting to
install a whole OS to try it, and decided I should do it in Docker
instead. Changing entire userspaces simply by naming a different image
is what Docker does, after all.

Note that this approach works around most of the awesome things about
sbt and probably makes builds take way longer. But it worked for me, a
complete outsider to Scala.

3.1 Dockerfile.build-with-sbt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: Dockerfile

    FROM adoptopenjdk/openjdk8
    ENV SCALA_VERSION 2.12.12
    ENV SBT_VERSION 1.3.8

    RUN \
    apt-get update && apt-get -y install npm docker.io webpack
    # my host docker group has gid 114
    RUN groupadd -g 5000 appuser && groupmod -g 114 docker && useradd -m -g 5000 -G docker -u 5000 appuser
    USER appuser
    WORKDIR /home/appuser
    VOLUME /home/appuser/Cortex
    VOLUME /home/appuser/.ivy2
    VOLUME /home/appuser/.sbt
    VOLUME /home/appuser/.cache

3.2 running build
~~~~~~~~~~~~~~~~~

.. code:: sh

    docker build -f Dockerfile.build-with-sbt -t sbt
    docker run -v /home/me/Cortex:/home/appuser/Cortex -v /home/me/.ivy2:/home/appuser/.ivy2 -v /home/me/.sbt:/home/appuser/.sbt -v /home/me/.cache:/home/appuser/.cache -v /var/run/docker.sock:/var/run/docker.sock -it sbt:latest

You can't use an NFS directory as the source of a volume (/home/me has
to be on a local disk).

npm ELIFECYCLE? `Remove some stuff and rebuild <https://stackoverflow.com/a/49505612>`_:

.. code:: sh

    cd Cortex/www
    npm cache clean --force
    rm package-lock.json
    rm -rf node_modules

3.3 running build from Emacs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This makes sbt stop with the colorization, and replaces paths inside
the container with paths outside, so that errors point at files Emacs
can open.

.. code:: sh

    docker run -v /home/me/Cortex:/home/appuser/Cortex -v /home/me/.ivy2:/home/appuser/.ivy2 -v /home/me/.sbt:/home/appuser/.sbt -v /home/me/.cache:/home/appuser/.cache -v /var/run/docker.sock:/var/run/docker.sock -it sbt:latest sh -c 'cd Cortex; ./sbt -Dsbt.log.noformat=true docker:stage' | sed 's,/home/appuser,/home/me,g'

3.4 getting image
~~~~~~~~~~~~~~~~~

output is in target/docker/stage. go there, and then:

.. code:: sh

    docker build . -t cortex && \
    docker tag cortex registry.k.my.domain/cortex && \
    docker push registry.k.my.domain/cortex

4 analyzer job input/output
---------------------------

Cortex needs to write input files for the job, the job needs to write
output files, and Cortex needs to read them. A persistent shared
filesystem fulfills these requirements.

4.1 HDFS (no)
~~~~~~~~~~~~~

Didn't end up doing this, but I saved the links I visited.

`newest HDFS on Kubernetes I could find, from 2019
<https://github.com/apache-spark-on-k8s/kubernetes-HDFS/blob/master/charts/README.md>`_. oops,
that one's taken down. `GCHQ HDFS
<https://gchq.github.io/gaffer-docker>`_. eh that one is not very
flexible. `gradiant/hdfs
<https://artifacthub.io/packages/helm/gradiant/hdfs>`_. jfrog thinks
it has vulnerabilities, iirc.

I believe TheHive (circa 4.0.1) supports storing artifacts on HDFS,
for cases where you need the scalability and can pay the complexity. I
looked into how it supports HDFS and it would need to be generalized
to make Cortex use HDFS for jobs.

4.2 ReadWriteMany
~~~~~~~~~~~~~~~~~

Shuffle the problem off to Kubernetes! That's what it's there
for. Just tell it you need a ReadWriteMany persistent volume
claim. How that is actually provided is not Cortex's business.

On a trivial cluster with a single node, it can be a local path:

.. code:: yaml

    apiVersion: v1
    kind: PersistentVolume
    metadata:
      namespace: job
      name: hppv
      labels:
        type: local
    spec:
      storageClassName: manual
      capacity:
        storage: 10Gi
      accessModes:
        - ReadWriteMany
      hostPath:
        path: "/mnt/data"

On a multinode self-hosted cluster, Longhorn 1.1 can reputedly provide
such a volume using NFS under the hood. Amazon and Azure have specific
ways of providing this. VMware can provide one. Etc.

To use such a volume, first make a claim:

.. code:: yaml

    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: hppvc
      namespace: job
    spec:
      storageClassName: manual
      accessModes:
        - ReadWriteMany
      resources:
        requests:
          storage: 3Gi

Then make some containers use it. This example shows mounting
subdirectories; this should enable jobs to get at the smallest needed
set of files while letting Cortex get at the whole thing.

.. code:: yaml

    apiVersion: batch/v1
    kind: Job
    metadata:
      name: copy-input-to-output
      namespace: job
    spec:
      template:
        spec:
          volumes:
          - name: hppvc
            persistentVolumeClaim:
              claimName: hppvc
          containers:
          - name: cito
            env:
            - name: JOBID
              value: "01"
            image: busybox
            command:
              - "rm"
              - "/job/input/hi"
            volumeMounts:
            - mountPath: /job/input
              name: hppvc
              subPathExpr: "$(JOBID)/input"
              readOnly: true
            - mountPath: /job/output
              name: hppvc
              subPathExpr: "$(JOBID)/output"
          restartPolicy: Never

5 running Cortex
----------------

5.1 OpenDistro for Elasticsearch using Helm (no)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As far as I've heard on the Discord, OpenDistro is not supported by
TheHive project, and no one has gotten it working yet. I decided to
try it. It didn't work. See farther down for why. I kept the shell
script I wrote, in case it comes in useful in the future.

https://opendistro.github.io/for-elasticsearch-docs/docs/install/helm/

.. code:: sh

    helm install -n cortex es opendistro-es-1.13.0.tgz --set global.clusterName=cortexes,kibana.enabled=false
    kubectl run -n cortex curl --image=curlimages/curl -- -XGET https://es-opendistro-es-client-service:9200 -u 'admin:admin' --insecure
    kubectl logs -n cortex curl

5.1.1 Certs
^^^^^^^^^^^

That worked, but now we need certs. Elastic Cloud on Kubernetes (ECK)
would do this for us automatically, but it is under the Elastic
License; I've set out to put Cortex atop ODFE in order to experiment
with avoiding that license. And Amazon has no motivation to make a
Kubernetes operator like ECK, because nice management for
Elasticsearch solely within their cloud is the thing they charge money
for, the reason they forked ODFE. An operator would let you use
someone else's cloud.

So manual cert generation it is. Or was, till I wrote this awesome
shell script.

.. code:: sh

    #!/bin/sh -xe

    CLUSTER_NAME=cluster.local # not sure how to find this
    NS=cortex
    NS_SVC="${NS}.svc.${CLUSTER_NAME}"
    ES_HELM_RELEASE=es
    ES_HELM_CHART=opendistro-es
    certs="client_svc"
    client_svc_ADD=client-service
    client_svc_CERT_BASENAME=elk-rest
    CA_NAME="${CLUSTER_NAME} ${NS} ${ES_HELM_RELEASE} ODFE Root CA"

    _secret () {
        eval $(echo "echo \${${1}_ADD}-certs")
    }
    _shn () {
        eval $(echo "echo ${ES_HELM_RELEASE}-${ES_HELM_CHART}-\$${1}_ADD")
    }
    _cbn () {
        eval $(echo "echo \${${1}_CERT_BASENAME}")
    }

    clean () {
      rm -rf ca client_svc
      kubectl delete secret -n ${NS} $(_secret client_svc) || \
          echo "- (error ignored)"
      exit 0
    }

    create_ca () {
        mkdir ca
        cd ca
        mkdir certs crl newcerts
        touch index.txt
        head -c 4 /dev/urandom | od -t u4 -An | tr -d ' ' > serial
        cat > openssl.cnf <<EOF
    [ ca ]
    default_ca = CA_default

    [ CA_default ]

    dir = .
    certs = \$dir/certs
    crl_dir = \$dir/crl
    database = \$dir/index.txt
    new_certs_dir = \$dir/newcerts
    certificate = \$dir/ca.pem
    serial = \$dir/serial
    crlnumber = \$dir/crlnumber
    crl = \$dir/crl.pem
    private_key = \$dir/ca.key
    x509_extensions = usr_cert
    name_opt = ca_default
    cert_opt = ca_default
    default_days = 730
    default_md = default
    preserve = no
    policy = idontcare

    [ idontcare ]

    [ usr_cert ]

    basicConstraints=CA:FALSE
    subjectKeyIdentifier=hash
    authorityKeyIdentifier=keyid,issuer
    keyUsage = nonRepudiation, digitalSignature, keyEncipherment

    EOF
        pwgen -s 32 1 > passphrase.txt
        openssl req -newkey rsa:4096 -keyout ca.key \
                -passout file:passphrase.txt -out ca.crt \
                -subj "/CN=${CLUSTER_NAME} ${NS} ${ES_HELM_RELEASE} ODFE Root CA" \
                -x509 -days +3650 -sha256
        cd ..
    }

    issue_cert () {
        shn=$(_shn $1)
        cbn=$(_cbn $1)
        fqdn="${shn}.${NS_SVC}"
        mkdir $1
        cd $1
        cat > req.conf <<EOF
    [req]   
    prompt=no
    utf8=yes
    distinguished_name=dn_details
    req_extensions=san_details
    [dn_details]
    CN=${fqdn}
    [san_details]
    subjectAltName=DNS:${fqdn},DNS:${shn}
    EOF
        openssl req -newkey rsa:4096 -keyout ${cbn}-key.pem -nodes \
                -subj "/CN=${fqdn}" -out ${cbn}-csr.pem -config req.conf
        cd ../ca
        openssl ca -keyfile ca.key -cert ca.crt -passin file:passphrase.txt \
                -in ../${cert}/${cbn}-csr.pem -out ../${cert}/${cbn}-crt.pem \
                -notext -batch -config openssl.cnf -extfile ../${cert}/req.conf \
                -extensions san_details
        cd ..
        cp ca/ca.crt $1/${cbn}-root-ca.pem
    }

    create_secret () {
        kubectl create secret generic -n ${NS} $(_secret $1) \
                --from-file=$1
        kubectl patch -n ${NS} secret $(_secret $1) \
                -p '{"metadata":{"labels":{"app":"elasticsearch"}}}'
    }

    if [ "$1" = clean ]; then
        clean
        exit 0
    fi

    create_ca
    for cert in ${certs}; do
        issue_cert $cert
        create_secret $cert
    done

#+name es-values.yaml

.. code:: yaml

    ---
    global:
      clusterName: cortexes
    kibana:
      enabled: false
    elasticsearch:
      imagePullPolicy: IfNotPresent
      ssl:
        rest:
          enabled: true
          existingCertSecret: client-service-certs
        transport:
          existingCertSecret: transport-certs
      config:
        opendistro_security.ssl.http.enabled: true
        opendistro_security.ssl.http.pemcert_filepath: elk-rest-crt.pem
        opendistro_security.ssl.http.pemkey_filepath: elk-rest-key.pem
        opendistro_security.ssl.http.pemtrustedcas_filepath: elk-rest-root-ca.pem
        opendistro_security.ssl.transport.pemcert_filepath: elk-transport-crt.pem
        opendistro_security.ssl.transport.pemkey_filepath: elk-transport-key.pem
        opendistro_security.ssl.transport.pemtrustedcas_filepath: elk-transport-root-ca.pem
    ...

.. code:: sh

    sh build.sh clean
    sh build.sh
    helm uninstall -n cortex es
    helm install -n cortex es opendistro-es-1.13.0.tgz -f es_values.yaml

5.1.2 Troubles
^^^^^^^^^^^^^^

The certificates are specified in the Helm values by purpose
(transport, REST API, admin, etc), and configured the same. But the
exceptions raised evince that the subject names that need to be in the
certs belong not to purposes, but to *services* (discovery, data-svc,
client-service). This reduces my confidence in the goodness of the
Helm charts.

I read some introductory documentation about creating an operator. No
big deal, right? I'll just learn another language and two more APIs...

No. For now I'm doing ECK. I've used it before, and it was easy and
fast. ODFE is a side quest; what I'm trying to do is get a working
Cortex.

5.2 ECK
~~~~~~~

`Quickstart <https://www.elastic.co/guide/en/cloud-on-k8s/1.4/k8s-quickstart.html#k8s-quickstart>`_

.. code:: sh

    kubectl apply -f https://download.elastic.co/downloads/eck/1.4.0/all-in-one.yaml

.. code:: yaml

    ---
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: esquickstart
      namespace: cortex
    spec:
      version: 7.10.2
      nodeSets:
      - name: default
        count: 1
        config:
          node.store.allow_mmap: false
    ...

And done. (I had to back off from 7.11 because of a compatibility
problem that's since been fixed; look on
https://blog.thehive-project.org/ around March 2021 for details.)

5.3 Cortex
~~~~~~~~~~

.. code:: yaml

    ---
    apiVersion: v1
    kind: Service
    metadata:
      namespace: cortex
      name: cortex-web-ui
    spec:
      selector:
        app: cortex
      ports:
        - protocol: TCP
          port: 80
          targetPort: 9001
    ...
    ---
    apiVersion: v1
    kind: PersistentVolume
    metadata:
      namespace: cortex
      name: cortex-hppv
      labels:
        type: local
    spec:
      storageClassName: manual
      capacity:
        storage: 10Gi
      accessModes:
        - ReadWriteMany
      hostPath:
        path: "/mnt/data"
    ...
    ---
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: hppvc
      namespace: cortex
    spec:
      storageClassName: manual
      accessModes:
        - ReadWriteMany
      resources:
        requests:
          storage: 3Gi
    ...
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      namespace: cortex
      name: cortex
      labels:
        app: cortex
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: cortex
      template:
        metadata:
          labels:
            app: cortex
        spec:
          serviceAccountName: cortex
          volumes:
          - name: jobdir
            persistentVolumeClaim:
              claimName: hppvc
          - name: es-http-ca
            secret:
              secretName: esquickstart-es-http-ca-internal
              items:
              - key: tls.crt
                path: es-http-ca.crt
          containers:
          - name: cortex
            image: registry.k.my.domain/cortex
            env:
              - name: es_uri
                value: https://esquickstart-es-http:9200
              - name: es_http_ca_cert
                value: /opt/cortex/es-http-ca/es-http-ca.crt
              - name: es_username
                value: elastic
              - name: es_password
                valueFrom:
                  secretKeyRef:
                    name: esquickstart-es-elastic-user
                    key: elastic
              - name: kubernetes_job_pvc
                value: hppvc
            volumeMounts:
            - mountPath: /tmp/cortex-jobs
              name: jobdir
            - mountPath: /opt/cortex/es-http-ca
              name: es-http-ca
    ...
    ---
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      namespace: cortex
      name: cortex-web-ui
    spec:
      rules:
      - host: cortex.k.my.domain
        http:
          paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: cortex-web-ui
                port:
                  number: 80
    ...

runs, but jobs don't run yet.

5.4 Service account
~~~~~~~~~~~~~~~~~~~

Create a role and a service account to enable Cortex's use of
Kubernetes.

.. code:: yaml

    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      namespace: cortex
      name: job-runner
    rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["get", "list"]
    - apiGroups: ["batch"]
      resources: ["jobs"]
      verbs: ["create", "delete", "get", "list", "watch"]
    ...
    ---
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: cortex
      namespace: cortex
    secrets:
    - name: default-token-lzm9h
    ...
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: cortex-job-runner
      namespace: cortex
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: Role
      name: job-runner
    subjects:
    - kind: ServiceAccount
      name: cortex
      namespace: cortex
    ...

And with that, jobs are created.
