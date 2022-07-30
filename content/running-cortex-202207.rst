Running Cortex again
####################
:date: 2022-07-26 21:53
:author: jaredj
:category: Security
:tags: cortex, kubernetes, docker, registry

So I have a brand new empty k3s server, and I've successfully built a
Docker image of Cortex. I need a registry to sock it in. OK, go find
my `registry instructions <cortex-on-kubernetes>`_, and hey prest---

.. code:: sh

    $ helm install registry twuni/docker-registry --set ingress.enabled=true,ingress.hosts\[0\]=registry.k.my.domain
    Error: INSTALLATION FAILED: unable to build kubernetes objects from release manifest: resource mapping not found for name: "registry-docker-registry" namespace: "" from "": no matches for kind "Ingress" in version "extensions/v1beta1"
    ensure CRDs are installed first

Ugh. Now, I happen to know this is because the Ingress API object is
gone from beta; you have to use the "extensions/v1" namespace for
it. That means the Helm chart I am trying to use has bit-rotted.

Oh would you look at that (``helm install --debug --dry-run ...``), I
was using version 1.2.0 of the chart because it was cached, and
version 2.1.0 is out. I just had to ``helm repo update`` and now I'm
using 2.1.0. And hey presto, it installed with just the command
above. Next hurdle!

OK, continuing with the Cortex on Kubernetes instructions, I've told
Docker my registry is insecure and -- Traefik is not directing me to
it despite the presence of an Ingress object. Oh gee look the ingress
class is nginx. Ok -

.. code:: sh

    helm upgrade registry twuni/docker-registry \
         --set ingress.enabled=true,\
         ingress.hosts\[0\]=registry.k.my.domain,\
         ingress.className=

(While the documentation for the traefik Helm chart included with k3s
appears to say that if I use ingress class name "traefik" it will
work, that didn't work, and an empty ingress class name did work.)

Now I can ``docker tag 0123456789abcdef
registry.k.my.domain/cortex:latest``, and ``docker push
registry.k.my.domain/cortex:latest``, and that works.

I didn't do the thing my earlier blog post says I had to about getting
k3s to use plaintext http with my registry, so gotta do that - k.

Um - maybe now I can use my helm-cortex chart? Ah - the persistent
volume is missing, ok, created that; now the secret
thc-es-http-certs-public is not found, because I took no time at all
to set up all the same certs I had last time. Actually - wait, that's
because the Cortex chart doesn't set up Elasticsearch, and I didn't
either. Oops. Gotta go install ECK. Hope it's still free-to-use.
`Deploying with ECK 2.3
<https://www.elastic.co/guide/en/cloud-on-k8s/2.3/k8s-deploy-eck.html>`_. 

.. code:: sh

    kubectl apply -f https://download.elastic.co/downloads/eck/2.3.0/crds.yaml
    kubectl apply -f https://download.elastic.co/downloads/eck/2.3.0/operator.yaml

That was easy. Of course they recommend I not use the default
Kubernetes namespace. Yes, I suppose.

.. code:: sh

    helm uninstall cortex
    kubectl create ns thehive
    kubectl apply -f es.yaml
    kubectl get pod -n thehive
    # wait a bit while it inits
    helm install cortex . -f values-as-given.yaml -n thehive
    
(es.yaml is an old file I had laying around from last time, describing
an Elasticsearch custom resource named thc of version 7.11.2 with one node.)

Along the way I noticed everything was at least 17 minutes old, and
installed OpenNTPD on my k3s server. (Chrony depended on GnuTLS, which
failed to install, and I hear bad things about GnuTLS from
cryptographers anyway. Last I checked, OpenNTPD had some snooty
opinions about which parts of the standard they would implement, but
that won't matter for me with one box at home.)

And now I find that my insecure registry pulling configuration didn't
take. Guess I have to restart k3s. Eyy nice! Cortex got pulled.

Now, it is failing its readiness and liveness tests, because the
container is refusing connections on port 9001. That could be
configuration, or it could be bad code. I wasn't even sure when I
started this round of building that it would build - I'm only half
done rescuing my Kubernetes Job pull request from bitrot... Let's look
at the logs. It's connected to Kubernetes for job running, it's
listening on 9001, it's timing out connecting to thc-es-http
port 9200. But after that it's got access logs for / getting hit -- oh
right, ``kubectl describe`` says those checks were failing several
minutes ago, not now. Ah nice, I have a webpage from Cortex in my
browser, with an error about Elasticsearch being unavailable. Fetched
through the Traefik attached to the k3s cluster. Ah, ES is
CrashLoopBackOff. Ah, ::

    [1]: max file descriptors [4096] for elasticsearch process is too low, increase to at least [65535]

I found that for a process with pid 12345, I could see the limits that
apply to it with ``cat /proc/12345/limits``.

The way to set limits for every process in Alpine is to set a value
for ``rc_ulimit`` in ``/etc/rc.conf``; but comments there recommend
that you instead do it within the scope of individual OpenRC services
that need it by instead setting that variable in ``/etc/conf.d/foo``,
for service foo. The value of this variable is just passed to the
``ulimit`` command. So I created ``/etc/conf.d/k3s``, containing
this::

    rc_ulimit="-n 65536"

and restarted k3s, ``service k3s restart``. Then I deleted the
``thc-es-whatnot`` pod, and when the appropriate controller made
another one, I looked for the java process running Elasticsearch,
inspected its limits, and I could see the number of open files was
raised to 65536.

With that set, Elasticsearch passed its boot-time checks and started
up. Cortex talked to it and brought up its initial "I need to update
the database" button and "Please create an admin user" page. I've
already seen Cortex fail to fetch the ``analyzers.json`` file, and I
didn't finish the Job code, so I don't think it will run an analysis
properly. That's a matter for further development. And so that's a
good place to wrap this post!
