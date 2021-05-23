Installing TheHive and Cortex using Helm on Kubernetes
######################################################
:date: 2021-03-25 09:57
:author: jaredj
:category: Projects

You don't have to do it exactly this way, but this is a reference.

 1. Obtain and install k3s following directions from k3s.io, including
    built-in Traefik.
 2. Install Helm as per k3s directions. (They just point you to
    directions at helm.sh.)
 3. Install ECK as per its directions.
 4. Create thehive namespace. ::

      kubectl create ns thehive
 
 5. Create an Elasticsearch cluster. ::

      kubectl apply -f - <<EOF
      apiVersion: elasticsearch.k8s.elastic.co/v1
      kind: Elasticsearch
      metadata:
        namespace: thehive
        name: thc
      spec:
        version: 7.11.2
        nodeSets:
        - name: default
          count: 1
          config:
            node.store.allow_mmap: false
      EOF
        
 6. Create a local-path persistent volume for Cortex job I/O. ::

      kubectl apply -f - <<EOF
      apiVersion: v1
      kind: PersistentVolume
      metadata:
        namespace: thehive
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
      EOF

 7. Install Cortex. ::

      git clone https://github.com/jaredjennings/helm-cortex
      cd helm-cortex
      helm install cortex . --namespace thehive \
                   --set elasticsearch.eck.enabled=true \
                   --set elasticsearch.eck.name=thc \
                   --set image.repository=jaredjennings/cortex \
                   --set jobIOStorage.pvc.storageClass=manual \
                   --set 'ingress.hosts[0].host=cortex.k.my.domain' \
                   --set 'ingress.hosts[0].paths[0].path=/' 

 8. Visit the cortex.k.my.domain page, click "update database," set up
    the admin user, set up an organization, and make a user with an
    API key.

 9. List the services. ::

      kubectl get service -n thehive

 10. My service is called cortex, so the url is going to be
     ``http://cortex:9000/``.  Given API key bar (it will really be a
     fairly long Base64 looking string), ::
 
      kubectl create secret generic -n thehive cortex-cardgage-api \
              --from-literal='urls=http://cortex:9001/' \
              --from-literal='keys=foo' 

 11. Install TheHive, with trivial local storage defaults. ::

      cd .. # out of helm-cortex
      git clone https://github.com/jaredjennings/helm-thehive
      cd helm-thehive
      helm install thehive . --namespace thehive \
                   --set storageClass=local-path \
                   --set cortex.enabled=true \
                   --set cortex.secret=cortex-cardgage-api \
                   --set 'ingress.hosts[0].host=thehive.k.my.domain' \
                   --set 'ingress.hosts[0].paths[0].path=/' 
                   
 12. Some kind of folderol with long startup times. Not sure exactly
     what.

 13. Log into TheHive using the default login. Set an org and user up.


Promblems with this setup
-------------------------

(I swear Strong Bad said "promblem" once, but I can't find it. EDIT: `aha! <https://homestarrunner.com/sbemails/170-rough-copy>`_)

 * Both web UIs are served over unencrypted HTTP. This is a matter of
   some Traefik twiddling, I think?
 * I think I got lucky about the Cortex connection: my cortex hostname
   is cortex, and the default hostname from the entrypoint is
   cortex. It doesn't appear to pay proper attention to
   ``TH_CORTEX_URLS``...?
 * This is trivially small. Neither Cassandra nor Elasticsearch (for
   TheHive) is involved.
 * Most of the challenges for users of late have been around
   migrations and upgrades; these Helm charts do nothing whatsoever
   about that.
