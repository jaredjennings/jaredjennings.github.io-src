An HTTPS registry in Kubernetes
###############################
:date: 2021-10-13 11:28
:author: jaredj
:category: Cloud
:tags: docker, kubernetes, registry, containers, k3s

`Earlier <cortex-on-kubernetes.html>`_ I set up a container registry
with plaintext HTTP. Now I want to set one up with HTTPS. It's still
internal, and I don't care yet about scanning containers for security
vulnerabilities, nor limiting who can fetch them. So it's still the
Docker registry, but with proper HTTPS.

This is still under k3s with Traefik 1.7 and configuration expressed
using Ingress resources.

 1. Generate the config that will request a DNS SAN for the certificate.

     cat <<ITS_OVER > csr.cnf
     # thanks http://blog.endpoint.com/2014/10/openssl-csr-with-alternative-names-one.html

     [req]
     default_bits = 2048
     prompt = no
     default_md = sha256
     req_extensions = req_ext
     distinguished_name = dn

     [dn]
     C=US
     ST=A State
     L=A City
     O=My Org
     OU=IT
     CN=registry.k.mydns.domain

     [req_ext]
     subjectAltName = @alt_names

     [alt_names]
     DNS.1=registry.k.mydns.domain
     ITS_OVER

 2. Generate a private key and CSR.

     openssl req -new -nodes -newkey rsa:2048 \
         -keyout registry.key -sha256 -config csr.cnf > registry.csr

 3. Issue the cert.
 4. Create a TLS secret with the good stuff in it.

     kubectl create secret tls -n registry registry-locally-issued \
         --cert=registry.crt --key=registry.key

 5. The raw Ingress resource with `TLS <https://kubernetes.io/docs/concepts/services-networking/ingress/#tls>`_ spec would look like this. (Don't do anything.)

.. code:: sh

     kubectl apply -f - <<ITS_OVER
     ---
     apiVersion: networking.k8s.io/v1
     kind: Ingress
     metadata:
       namespace: registry
       name: registry
     spec:
       tls:
         - hosts:
             - registry.k.mydns.domain
           secretName: registry-locally-issued
       rules:
         - host: registry.k.mydns.domain
           http:
             paths:
               - path: /
                 pathType: Prefix
                 backend:
                   service:
                     name: registry
                     port:
                       number: 80
       ITS_OVER

  6. The Helm chart takes care of it. Do this:

       cat > registry-values.yaml <<ITS_OVER
       ingress:
         enabled: true
         hosts:
           - registry.k.mydns.domain
         tls:
           - hosts:
               - registry.k.mydns.domain
             secretName: registry-locally-issued
       persistence:
         enabled: true
       ITS_OVER

       helm install -n registry registry twuni/docker-registry \
           --values registry-values.yaml
