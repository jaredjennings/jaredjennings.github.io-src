TheHive and Cortex on Kubernetes with Helm, late May 2021
#########################################################
:date: 2021-05-21 16:26
:author: jaredj
:tags: kubernetes, thehive, cortex, helm

What's new?
-----------

- TheHive storing data in Cassandra and Elasticsearch.
- Support for adding arbitrary bits of configuration.
- I managed to configure single signon using OIDC with Keycloak.

Our story so far
----------------

We're on my single-node k3s cluster, described `previously
<installing-thehive-and-cortex-using-helm-on-kubernetes.html>`_. Keycloak
is installed `like so <keycloak-12-on-kubernetes.html>`_. Let us
assume TheHive and Cortex to *not* be installed (that's easy for me:
I've done a ton of ``hive uninstall`` and ``hive install`` lately).

Keycloak setup
--------------

In Keycloak I've set up a realm. Now, I'm quite new to Keycloak, so
I've noodled around quite a bit. The Keycloak Operator supports doing
this stuff in a more Kubernetes way; it would be cool to do that in
the future, not least because I've probably forgotten a noodle or two
here.

Anyway, I logged into Keycloak as admin. My Keycloak is in the
Kubernetes namespace ``my-keycloak-operator``; in that namespace is a
secret called ``credential-mykeycloak`` with the admin password in
it. To get it out::

    kubectl get secret -n my-keycloak-operator credential-mykeycloak -o 'jsonpath={.data.ADMIN_PASSWORD}' | base64 -d

Or, more unixily, perhaps::

    kubectl get secret -n my-keycloak-operator credential-mykeycloak -o json | jq -r '.data.ADMIN_PASSWORD' | base64 -d

Doesn't really matter either way—I just type Ctrl-R ADMIN and my shell
searches it out of history.

So I created a Realm in Keycloak, and a local user therein by the name
of ``jjc@example.com``. (Keycloak of course supports the finding and
authentication of users using other systems; all of those are out of
scope for my initial learning.) Also in Cortex I created the user.

Cortex Keycloak client setup
----------------------------

To create a Client, I first made an `initial access token
<https://www.keycloak.org/docs/latest/securing_apps/#_initial_access_token>`_,
then pasted it in a `curl command
<https://www.keycloak.org/docs/latest/securing_apps/#example-using-curl-2>`_
which included a desired client ID—I used ``cortex`` for Cortex. This
yielded some JSON; one of the values therein was the client secret,
which is a GUID (randomly generated example:
``b2a3ae28-3eb1-4ccb-983a-c46ace2b125a``). Following the `Cortex
documentation on OIDC
<https://github.com/TheHive-Project/CortexDocs/blob/master/admin/admin-guide.md#authentication>`_,
I plugged those values into an SSO configuration for Cortex.

Cortex SSO configuration
------------------------

I started having enough values for Helm that I quit using ``--set``
command line options and started writing the values in a file
``values-as-given.yaml``, handing it to Helm with the ``-f``
switch. In that file - ::

    extraCortexConfigurations:
       'authn-oauth2.conf': |
          auth {
              provider = [local, oauth2]
              sso {
                autocreate: false
                autoupdate: false
                mapper: "simple"
                attributes {
                  login: "email"
                  name: "name"
                  roles: "resource_access.cortex.role"
                  organization: "cortexorg"
                }
                defaultRoles: ["read", "analyze"]
                defaultOrganization: "demo"
              }
              oauth2 {
                name: oauth2
                clientId: "cortex"
                clientSecret: "deadbeef-bead-cafe-0123-ffffffffffff"
                redirectUri: "https://cortex.k.my.dns.domain/api/ssoLogin"
                responseType: "code"
                grantType: "authorization_code"
                authorizationUrl: "https://keycloak.k.my.dns.domain/auth/realms/cortex/protocol/openid-connect/auth"
                authorizationHeader: "Bearer"
                tokenUrl: "https://keycloak.k.my.dns.domain/auth/realms/cortex/protocol/openid-connect/token"
                userUrl: "https://keycloak.k.my.dns.domain/auth/realms/cortex/protocol/openid-connect/userinfo"
                scope: ["email", "name", "cortexorg"]
                userIdField: "email"
                }
            }

Cortex needs to be able to trust the Keycloak server's certificate. In
the values-as-given::

    trustRootCerts:
      - |
        -----BEGIN CERTIFICATE-----
        MIIFKz...
        -----END CERTIFICATE-----

If this is not properly in place, SSO will not work and *you will not
get any log messages about why*.

Cortex bringup
--------------

Besides the above values, my ``values-as-given.yaml`` ended up with
these too::

    image:
      repository: registry.k.my.dns.domain/cortex
      pullPolicy: Always
      tag: latest
    elasticsearch:
      eck:
        enabled: true
        name: thc
    image:
      repository: registry.k.my.dns.domain/cortex
    ingress:
      hosts:
      - host: cortex.k.my.dns.domain
        paths:
        - path: /
    jobIOStorage:
      pvc:
        storageClass: manual

Most of these are values provided by ``--set`` switches on the command
line in previous Cortex installs. So now the Cortex install looks
like::

    cd .../helm-cortex
    helm install cortex . --namespace thehive -f values-as-given.yaml

TheHive Keycloak client setup
-----------------------------

Exactly the same as for Cortex. I used the client ID "thehive." Notate
the client secret, and plug it into the Hive config. I used the same
realm as before, which I called ``cortex``. Maybe not a very good
name. In a ``values-as-given.yaml`` for helm-thehive, separate from
the one for Cortex::

    extraHiveConfigurations:
      'authn-oauth2.conf': |
        auth {
          providers: [
            {name: session}
            {name: basic, realm: thehive}
            {name: local}
            {name: key}
            {
              name: oauth2
              clientId: "h2-thehive"
              clientSecret: "ffffffff-ffff-ffff-ffff-ffffffffffff"
              redirectUri: "https://h2.k.my.dns.domain/api/ssoLogin"
              responseType: "code"
              grantType: "authorization_code"
              authorizationUrl: "https://keycloak.k.my.dns.domain/auth/realms/cortex/protocol/openid-connect/auth"
              authorizationHeader: "Bearer"
              tokenUrl: "https://keycloak.k.my.dns.domain/auth/realms/cortex/protocol/openid-connect/token"
              userUrl: "https://keycloak.k.my.dns.domain/auth/realms/cortex/protocol/openid-connect/userinfo"
              scope: ["email", "name", "hiveorg"]
              defaultOrganisation: "cardgage"
              organisationField: "hiveorg"
              userIdField: "email"
            }
          ]
        }

(I took to calling my Helm release h2, to make sure all the templating
would work right even if you don't name it thehive.)

And the trust for the Keycloak cert::

    trustRootCerts:
      - |
        -----BEGIN CERTIFICATE-----
        MIIFKz...
        -----END CERTIFICATE-----

 Other values-as-given::

    ingress:
      hosts:
        - host: h2.k.my.dns.domzin
          paths:
           - path: /
    elasticsearch:
      eck:
        enabled: true
        name: thc
    cassandra:
      enabled: true
      persistence:
        storageClass: local-path
      dbUser:
        password: "my-super-secure-password"
    storageClass: local-path

TheHive bringup
---------------

::

    cd .../helm-thehive
    helm install -n thehive h2 . -f values-as-given.yaml

As far as I've seen, the first time TheHive starts, it won't be able
to contact Cassandra through multiple retries. Give it time.

