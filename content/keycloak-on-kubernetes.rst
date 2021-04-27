Keycloak 12 on Kubernetes
#########################
:date: 2021-04-27 15:51
:author: jaredj
:category: Projects

I'm trying to put a Keycloak in front of my Cortex 3, Hive 4, and MISP
2.4.140 Kubernetes deployments, to unify authentication decisions for
all of them. As in previous articles, I'm doing this on a small k3s
cluster; right now it is at version 1.20.2+k3s1. This version of k3s
includes Traefik 1.7, and that included version is what I'm using;
apparently the next one `will include Traefik 2
<https://github.com/k3s-io/k3s/issues/1141>`_ and all I've learned
here will be slightly different. Oh well.

I deployed Keycloak using the `operator
<https://www.keycloak.org/getting-started/getting-started-operator-kubernetes>`_. The
first hurdle is that it serves HTTPS, but Traefik would work much more
nicely with it if it would serve plaintext HTTP. But it doesn't.

I deployed the Keycloak cluster by adding this resource::

    apiVersion: keycloak.org/v1alpha1
    kind: Keycloak
    metadata:
      name: mykeycloak
      namespace: my-keycloak-operator
      labels:
        app: mykeycloak
    spec:
      instances: 1
      externalAccess:
        enabled: True

The externalAccess bit makes the operator construct an Ingress
object. That object has such annotations::

    metadata:
      annotations:
        nginx.ingress.kubernetes.io/backend-protocol: HTTPS

After a long while I learned that the
``ingress.kubernetes.io/protocol`` annotation needs to be *manually
added* to the Ingress to make Traefik 1.7 stop trying to use plaintext
HTTP to communicate with it::

    metadata:
      annotations:
        ingress.kubernetes.io/protocol: https
        nginx.ingress.kubernetes.io/backend-protocol: HTTPS

Now, Keycloak makes up a certificate, which of course Traefik doesn't
trust. The immediate — and *temporary* — fix is to edit the
``traefik`` deployment in the ``kube-system`` namespace, and add
``--insecureSkipVerify=true`` to the command-line arguments of
Traefik; or edit the ``traefik`` configmap in the ``kube-system``
namespace, and add ``insecureSkipVerify=true``. If you edit the
deployment, you get a restart for free.

The next thing to try is to set the ``rootCAs`` in the ``traefik``
configmap. But it seems Traefik is trying to get to the Keycloak
Service by means of its IP address, and there is of course no IP
address SAN in the certificate for that IP address.

After a jaunt through the source code of the Keycloak operator and
container scripts, I've pieced together how to specify a certificate
to use. This will probably not help with the IP SAN issue, but it will
help with the made-up-cert issue.

At `line 180 et seq
<https://github.com/keycloak/keycloak-operator/blob/0c760d38f9caa30cee8bf6a5b1c885ac23ac5d5d/pkg/model/keycloak_deployment.go#L180>`_
of ``keycloak-operator/keycloak_deployment.go``, the Keycloak
deployment object is laid out. It gets volume mounts for the container
from `KeycloakVolumeMounts
<https://github.com/keycloak/keycloak-operator/blob/0c760d38f9caa30cee8bf6a5b1c885ac23ac5d5d/pkg/model/keycloak_deployment.go#L297>`_,
which says that the volume having ``ServingCertSecretName`` as its
name should be mounted at ``/etc/x509/https``. Nearby,
`KeycloakVolumes
<https://github.com/keycloak/keycloak-operator/blob/0c760d38f9caa30cee8bf6a5b1c885ac23ac5d5d/pkg/model/keycloak_deployment.go#L332>`_
specifies that the contents of that volume should come from the secret
having ``ServingCertSecretName`` as its name. That `constant
<https://github.com/keycloak/keycloak-operator/blob/0c760d38f9caa30cee8bf6a5b1c885ac23ac5d5d/pkg/model/constants.go#L41>`_'s
value is ``"sso-x509-https-secret"``.

Now, the `Docker entrypoint
<https://github.com/keycloak/keycloak-containers/blob/d4ce446dde3026f89f66fa86b58c2d0d6132ce4d/server/tools/docker-entrypoint.sh>`_
for the Keycloak server image runs one `x509.sh
<https://github.com/keycloak/keycloak-containers/blob/d4ce446dde3026f89f66fa86b58c2d0d6132ce4d/server/tools/x509.sh>`_,
which takes the files ``tls.crt`` and ``tls.key`` from
``/etc/x509/https`` and makes a keystore out of them for Keycloak to
use.

So! To specify a certificate, make a usual TLS secret in the
appropriate namespace, with a tls.crt and tls.key inside. Call the
secret ``sso-x509-https-secret``.
