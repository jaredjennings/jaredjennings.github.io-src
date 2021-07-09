igrating from TheHive 3 to 4
#############################
:date: 2021-07-09 15:08
:author: jaredj

Preconditions
-------------

 1. It is mid-2021. TheHive 4.1 is current.
 2. TheHive 3.4.0, Cortex 3.0.0, and Elasticsearch 5.6.0 are installed
    on a single Linux server using packages. Let us call it `jimmy`.
 3. Elasticsearch only accepts connections from ``localhost``, and
    they are unauthenticated and unencrypted.
 4. Snapshots can be taken to a local directory.
 5. A Kubernetes cluster is set up. It provides persistent volumes
    using a ``storageClass`` of ``longhorn``.
 6. Elastic Cloud on Kubernetes (ECK) is already installed.
 7. Web proxy settings need not be specifically provided, but Web
    traffic goes through a filtering proxy that inspects TLS traffic
    by performing a MitM attack. Consequently, an additional
    organization-specific root CA must be trusted in order to get any
    HTTPS done.

Postconditions
--------------

 1. A ScyllaDB database has been set up.
 2. A Hive 4.1 instance is set up.
 3. Data (cases, observables, tasks) is stored in the ScyllaDB
    database and visible by TheHive 4.1.

Lemmas
------

In the course of this, a few things which may be interesting in their
own right are done:

 * Elasticsearch is deployed using ECK, pulling in the S3 snapshot
   plugin from behind a TLS-rewriting proxy.

Lorem ipsum
-----------

Example names and words chosen throughout this document are listed
here. If your configuration contains any of these strings, you may
need to replace them with values more specific to the context in which
you are working.

 * ``jimmy``
 * ``emili``
 * ``k.example.org``
 * ``example.org``
 * ``pY8Il9uhRxIh``
 * ``ateljevic``
 * ``jitendraa3``
 * ``changeit``. This is often used for Java trust stores, because the
   store password is not securing any private keys, but it's good
   to make something random.
 * ``ljungstrand``
 * ``pataki``
 * ``karstensen``


Relevant documentation
----------------------

 * `Migration from TheHive 3.x <http://docs.thehive-project.org/thehive/operations/migration/>`_
 * `3.4.x -> 3.5.0 migration guide <http://docs.thehive-project.org/thehive/legacy/thehive3/migration-guide/>`_

There are two paths outlined:

 - 3.4.x -> 3.5.x -> 4.1.x; or
 - 3.4.x -> 4.0.x -> 4.1.x.

Procedure
---------

Reindex ES5 data in ES6
.......................

 1. Take a snapshot, which we shall call `es5original`. On `jimmy`::

      curl -XPUT http://localhost:9200/_snapshot/local/es5original\?wait_for_completion=true

 2. Run a temporary `MinIO server
    <https://docs.min.io/docs/minio-quickstart-guide>`_ on some
    host. Let us refer to this host as `emili`. ::

      MINIO_ROOT_USER=ateljevic MINIO_ROOT_PASSWORD=jitendraa3 \
        ./minio server --address localhost:9300 /tmp/a_bucket

 3.  Run a `mc command-line client <https://docs.min.io/docs/minio-client-quickstart-guide>`_. Prompts for access key and secret key will show; these
     should be the values given for MINIO_ROOT_USER and
     MINIO_ROOT_PASSWORD from above.

 4. Place the Elastic snapshot data taken in step 1 inside the
    directory MinIO is serving.

 5. On your Kubernetes cluster, set up a Secret for Elasticsearch to
    get the credentials from. (Use the same values given above for
    MINIO_ROOT_USER and MINIO_ROOT_PASSWORD. ::

      kubectl create secret generic ephemeral-minio \
        --from-literal=s3.client.local_minio_snapshots.access_key=ateljevic \
        '--from-literal=s3.client.local_minio_snapshots.secret_key=jitendraa3'

 6. Create a Secret with the root CA that must be trusted in order to
    do HTTPS through the organization's filtering proxy. ::

      mkdir root-ca
      cat > root-ca/ca.crt <<ITSOVER
      ----- BEGIN CERTIFICATE ------
      pY8Il9uhRxIhRm5WehfcxZeLmXea7O6EszrYarwO+rmm/07jUS43wLZB+Js6xxQLJLeLDKMMuLFq
      jEma8ttQE1ZWhZjHYxwBziWagpFUp1jXauak4/OJrd6ijrmolTC1fmt9ff3T6R7w1qYqhs74/3ad
      [...]
      ----- END CERTIFICATE -----
      ITSOVER
      kubectl create secret generic root-ca --from-file=root-ca

 7. Write this description of the ElasticSearch 6 cluster into ``es6.yaml``. ::

      apiVersion: elasticsearch.k8s.elastic.co/v1
      kind: Elasticsearch
      metadata:
        namespace: hivemig
        name: es6
      spec:
        version: 6.8.12
        secureSettings:
          - secretName: ephemeral-minio
        nodeSets:
          - name: default
            count: 1
            config:
              node.master: true
              node.data: true
              node.ingest: true
              action.auto_create_index: .watches,.triggered_watches,.watcher-history-*
              s3.client.default.protocol: http
              s3.client.default.endpoint: "emili.example.org:9300"
            podTemplate:
              spec:
                volumes:
                  - name: trust
                    emptyDir: {}
                  - name: root-ca
                    secret:
                      secretName: root-ca
                initContainers:
                - name: sysctl
                  securityContext:
                    privileged: true
                  command: ['sh', '-c', 'sysctl -w vm.max_map_count=262144']
                # trust our root CA so we can fetch the s3 plugin from the web
                - name: trust-our-root
                  volumeMounts:
                    - name: trust
                      mountPath: /trust
                    - name: root-ca
                      mountPath: /root-ca
                  command: ['sh', '-c', '$(find /opt -name keytool | head -n 1) -import -keystore /trust/store -storetype jks -alias root-ca -file /root-ca/ca.crt -storepass changeit -trustcacerts -noprompt']
                - name: install-plugins
                  volumeMounts:
                    - name: trust
                      mountPath: /trust
                  env:
                    - name: ES_JAVA_OPTS
                      value: "-Djavax.net.ssl.trustStore=/trust/store -Djavax.net.debug=all"
                  command: ['sh', '-c', 'bin/elasticsearch-plugin install --batch repository-s3']
            volumeClaimTemplates:
            - metadata:
                name: elasticsearch-data
              spec:
                accessModes:
                - ReadWriteOnce
                resources:
                  requests:
                    storage: 10Gi
                storageClassName: longhorn

 8. Create the ES6 cluster including the S3 plugin using ECK. `Change
    your default namespace
    <https://www.kubernet.dev/set-a-default-namespace-for-kubectl/>`_. ::

      kubectl create ns hivemig
      kubectl config set-context --current --namespace=hivemig
      kubectl apply -f es6.yaml

 9. Tell the ES6 server about the snapshot repository. Note that the
    es6.yaml configures the default S3 client settings to point at
    ``emili``, and that default client is used for this repository. ::

      EPASS=$(kubectl get -o jsonpath='{.data.elastic}' secret es6-es-elastic-user | base64 -d)
      SVCIP=$(kubectl get svc es6-es-http -o jsonpath='{.spec.clusterIPs[0]}')
      curl -k -u elastic:$EPASS -XPUT -H 'content-type: application/json' \
        https://$SVCIP:9200/_snapshot/my_minio \
        -d '{"type":"s3", "settings":{ "bucket": "elastic_snapshots"}}'

 10. Tell the ES6 server to restore the snapshot. ::

      curl -k -u elastic:$EPASS https://$SVCIP:9200/_snapshot/my_minio/es5original
      curl -k -u elastic:$EPASS -XPOST https://$SVCIP:9200/_snapshot/my_minio/es5original/_restore

 11. Do the `reindexing
     <http://docs.thehive-project.org/thehive/legacy/thehive3/admin/upgrade_to_thehive_3_5_and_es_7_x/#create-a-new-index>`_
     in the 3.5.0 migration guide. ::

      curl -k -u elastic:$EPASS -XPUT "https://${SVCIP}:9200/new_the_hive_15" \
            -H 'content-type: application/json' \
            -d "$(curl -k -u elastic:$EPASS https://${SVCIP}:9200/the_hive_15 | jq '.the_hive_15 | del(.settings.index.provided_name, .settings.index.uuid, .settings.index.version, .settings.index.mapping.single_type, .settings.index.creation_date, .mappings.doc._all)')"
       curl -k -u elastic:$EPASS -XPOST \
            -H 'Content-type: application/json' https://$SVCIP:9200/_reindex \
            -d '{"conflicts":"proceed","source":{"index":"the_hive_15"}, "dest":{"index":"new_the_hive_15"}}'
       curl -k -u elastic:$EPASS -XPUT "https://${SVCIP}:9200/new_cortex_4" \
            -H 'content-type: application/json' \
            -d "$(curl -k -u elastic:$EPASS https://${SVCIP}:9200/cortex_4 | jq '.cortex_4 | del(.settings.index.provided_name, .settings.index.uuid, .settings.index.version, .settings.index.mapping.single_type, .settings.index.creation_date, .mappings.doc._all)')"
       curl -k -u elastic:$EPASS -XPOST \
            -H 'Content-type: application/json' https://$SVCIP:9200/_reindex \
            -d '{"conflicts":"proceed","source":{"index":"cortex_4"}, "dest":{"index":"new_cortex_4"}}'
       curl -k -u elastic:$EPASS -XPOST -H 'Content-Type: application/json' \
            "https://${SVCIP}:9200/_aliases" -d \
            '{"actions":[{"add":{"index":"new_the_hive_15","alias":"the_hive_15"}},{"add":{"index":"new_cortex_4","alias":"cortex_4"}}]}'

 12. Snap this as `es6reindex` into the MinIO S3 bucket. ::

       curl -k -u elastic:$EPASS -XPUT \
         "https://${SVCIP}:9200/_snapshot/my_minio/es6reindex?wait_for_completion=true"

Update database with TheHive 3.5.1
..................................

 13. Run ES7. Write the following into ``es7.yaml``, then run
     ``kubectl apply -f es7.yaml``. ::

       apiVersion: elasticsearch.k8s.elastic.co/v1
       kind: Elasticsearch
       metadata:
         namespace: hivemig
         name: es7
       spec:
         version: 7.10.2
         secureSettings:
           - secretName: ephemeral-minio
         nodeSets:
           - name: default
             count: 3
             config:
               node.master: true
               node.data: true
               node.ingest: true
               action.auto_create_index: .watches,.triggered_watches,.watcher-history-*
               s3.client.default.protocol: http
               s3.client.default.endpoint: "emili.example.org:9300"
             podTemplate:
               spec:
                 volumes:
                   - name: trust
                     emptyDir: {}
                   - name: root-ca
                     secret:
                       secretName: root-ca
                 initContainers:
                 - name: sysctl
                   securityContext:
                     privileged: true
                   command: ['sh', '-c', 'sysctl -w vm.max_map_count=262144']
                 # trust our root CA so we can fetch the s3 plugin from the web
                 - name: trust-our-root
                   volumeMounts:
                     - name: trust
                       mountPath: /trust
                     - name: root-ca
                       mountPath: /root-ca
                   command: ['sh', '-c', '$(find / -name keytool | head -n 1) -import -keystore /trust/store -storetype jks -alias root-ca -file /root-ca/ca.crt -storepass changeit -trustcacerts -noprompt']
                 - name: install-plugins
                   volumeMounts:
                     - name: trust
                       mountPath: /trust
                   env:
                     - name: ES_JAVA_OPTS
                       value: "-Djavax.net.ssl.trustStore=/trust/store -Djavax.net.debug=all"
                   command: ['sh', '-c', 'bin/elasticsearch-plugin install --batch repository-s3']
             volumeClaimTemplates:
             - metadata:
                 name: elasticsearch-data
               spec:
                 accessModes:
                 - ReadWriteOnce
                 resources:
                   requests:
                     storage: 10Gi
                 storageClassName: longhorn

 14. Tell ES7 about the snapshot repo. ::

       EPASS=$(kubectl get -o jsonpath='{.data.elastic}' secret es7-es-elastic-user | base64 -d)
       SVCIP=$(kubectl get svc es7-es-http -o jsonpath='{.spec.clusterIPs[0]}')
       curl -k -u elastic:$EPASS -XPUT -H 'content-type: application/json' \
            https://$SVCIP:9200/_snapshot/my_minio \
            -d '{"type":"s3", "settings":{ "bucket": "elastic_snapshots"}}'

 15. Restore the snapshot. ::

       curl -k -u elastic:$EPASS https://$SVCIP:9200/_snapshot/my_minio/es6reindex
       curl -k -u elastic:$EPASS -XPOST https://$SVCIP:9200/_snapshot/my_minio/es6reindex/_restore
       curl -k -u elastic:$EPASS https://$SVCIP:9200/_cat/indices\?v

 16. Install TheHive 3 using my Helm chart. Write the following YAML
     into ``values3.yaml``::

        image:
          repository: thehiveproject/thehive
          tag: "3.5.1-1"

        ingress:
          enabled: true
          hosts:
            - host: hive.k.example.org
              paths:
                - path: /

        elasticsearch:
          eck:
            enabled: true
            name: es7

     Then::

       helm install -n hivemig h3b helm-thehive -f values3.yaml

     If you don't already have a copy of the chart cloned::

       git clone https://github.com/jaredjennings/helm-thehive

 17. Visit http://hive.k.example.org. It will tell you it needs to
     update the database. Click the button. After it finishes you do
     not need to log in.

 18. Now, take a snapshot, which we shall call `th35upgrade`. ::

       curl -k -u elastic:$EPASS -XPUT \
         "https://${SVCIP}:9200/_snapshot/my_minio/th35upgrade?wait_for_completion=true"

 19. Snag the configuration from the running copy of TheHive 3. ::

       H3B_POD=$(kubectl get -o json pod | jq -r '.items[].metadata.name | select(startswith("th4"))')
       kubectl exec $H3B_POD -it -- bash
       find /etc/thehive | xargs cat
       # copy output to clipboard

     This will come in handy later when configuring the migration tool.

 20. Uninstall TheHive3. ::

       helm uninstall -n hivemig h3b

Prepare configuration files and databases for migrate script
............................................................

 21. Make a directory called ``migration-configs``. Put the Hive3
     configuration you grabbed into a file called ``hive3.conf``
     therein. ::

        play.http.secret.key = "ljungstrand pataki"

        search {
          index = the_hive
          uri = "https://es7-es-http:9200/"
          keepalive = 1m
          pagesize = 50
          nbshards = 5
          nbreplicas = 1
          connectionRequestTimeout = 120000
          connectTimeout = 120000
          socketTimeout = 120000
          settings {
            mapping.nested_fields.limit = 100
          }
          user = "elastic"
          password = "karstensen"
          keyStore {
            path = "/configs/store-es7"
            type = "JKS"
            # There are no private keys to protect in this trust
            # store, so its password need not actually secure it.
            password = "changeit"
          }
          trustStore {
            path = "/configs/store-es7"
            type = "JKS"
            # There are no private keys to protect in this trust
            # store, so its password need not actually secure it.
            password = "changeit"
          }
        }

     The password for the elastic user in the es7 cluster is in the
     ``es7-elastic-user`` Kubernetes secret. To get it out::

        kubectl get secret es7-es-elastic-user -o template='{{.data.elastic | base64decode}}'

 22. Construct a Cassandra database into which to migrate the data, as
     well as an Elasticsearch 7 instance.

     First follow directions in `Deploying Scylla on a Kubernetes
     Cluster
     <https://operator.docs.scylladb.com/stable/generic.html>`_. Then
     write ``scylla-cluster.yaml`` as follows::

       # ServiceAccount for scylla members.
       apiVersion: v1
       kind: ServiceAccount
       metadata:
         name: simple-cluster-member
         namespace: hivemig

       ---

       # RoleBinding for scylla members.
       apiVersion: rbac.authorization.k8s.io/v1
       kind: ClusterRoleBinding
       metadata:
         name: simple-cluster-member
         namespace: hivemig
       roleRef:
         apiGroup: rbac.authorization.k8s.io
         kind: ClusterRole
         name: scyllacluster-member
       subjects:
         - kind: ServiceAccount
           name: simple-cluster-member
           namespace: hivemig

       ---

       # Simple Scylla Cluster
       apiVersion: scylla.scylladb.com/v1
       kind: ScyllaCluster
       metadata:
         labels:
           controller-tools.k8s.io: "1.0"
         name: simple-cluster
         namespace: hivemig
       spec:
         version: 4.2.0
         agentVersion: 2.2.0
         developerMode: true
         datacenter:
           name: dc1
           racks:
             - name: dc1ra
               scyllaConfig: "scylla-config"
               scyllaAgentConfig: "scylla-agent-config"
               members: 3
               storage:
                 capacity: 5Gi
                 storageClassName: longhorn
               resources:
                 requests:
                   cpu: 1
                   memory: 1Gi
                 limits:
                   cpu: 1
                   memory: 1Gi
               volumes:
                 - name: coredumpfs
                   hostPath:
                     path: /tmp/coredumps
               volumeMounts:
                 - mountPath: /tmp/coredumps
                   name: coredumpfs
     
     Now ``kubectl apply -f scylla-cluster.yaml``.

 23. Bring up an Elasticsearch 7 cluster for TheHive4, imaginatively
     enough called ``es74h4``. This is the same as es7 but has a
     different name; also it will have its own certs and passwords. It
     doesn't need the S3 connection to do its job in this context;
     that's just there because I copied this entire file from
     above. Here's ``es74h4.yaml``::

        apiVersion: elasticsearch.k8s.elastic.co/v1
        kind: Elasticsearch
        metadata:
          namespace: hivemig
          name: es74h4
        spec:
          version: 7.10.2
          secureSettings:
            - secretName: ephemeral-minio
          nodeSets:
            - name: default
              count: 3
              config:
                node.master: true
                node.data: true
                node.ingest: true
                action.auto_create_index: .watches,.triggered_watches,.watcher-history-*
                s3.client.default.protocol: http
                s3.client.default.endpoint: "emili.example.org:9300"
              podTemplate:
                spec:
                  volumes:
                    - name: trust
                      emptyDir: {}
                    - name: root-ca
                      secret:
                        secretName: root-ca
                  initContainers:
                  - name: sysctl
                    securityContext:
                      privileged: true
                    command: ['sh', '-c', 'sysctl -w vm.max_map_count=262144']
                  # trust our root CA so we can fetch the s3 plugin from the web
                  - name: trust-our-root
                    volumeMounts:
                      - name: trust
                        mountPath: /trust
                      - name: root-ca
                        mountPath: /root-ca
                    command: ['sh', '-c', '$(find / -name keytool | head -n 1) -import -keystore /trust/store -storetype jks -alias root -file /root-ca/ca.crt -storepass changeit -trustcacerts -noprompt']
                  - name: install-plugins
                    volumeMounts:
                      - name: trust
                        mountPath: /trust
                    env:
                      - name: ES_JAVA_OPTS
                        value: "-Djavax.net.ssl.trustStore=/trust/store -Djavax.net.debug=all"
                    command: ['sh', '-c', 'bin/elasticsearch-plugin install --batch repository-s3']
                    # command: ['sh', '-c', 'true']
              volumeClaimTemplates:
              - metadata:
                  name: elasticsearch-data
                spec:
                  accessModes:
                  - ReadWriteOnce
                  resources:
                    requests:
                      storage: 10Gi
                  storageClassName: longhorn

 24. Drum up Hive4 configuration ("Once TheHive4 configuration file
     (/etc/thehive/application.conf) is correctly filled you can run
     migration tool."). So write ``values4.yaml`` as follows::
     
        ingress:
          enabled: true
          hosts:
            - host: hive.k.example.com
              paths:
                - path: /

        elasticsearch:
          eck:
            enabled: true
            name: es74h4

        storageClass: longhorn

        cassandra:
          enabled: false

        externalCassandra:
          enabled: true
          hostName: simple-cluster-client
          dbUser:
            name: cassandra
            password: authentication-not-used-right-now

     Then::

       helm template -n hivemig th4 helm-thehive -f helm-thehive/values4.yaml

     Grab the configuration from ``kubectl get configmap
     th4-thehive-etc-th-tmpl``, or actually ``helm install -n hivemig
     th4 helm-thehive -f values4.yaml``, then do the same ``kubectl
     exec ... -it bash`` seen above for grabbing Hive 3 configuration.

     As with previous Elasticsearch clusters, the password for the
     ``elastic`` user for this cluster is in its own
     ``es74h4-es-elastic-user`` secret.

 25. Get the CA certificates from both elasticsearch clusters and make
     truststores containing each. ::

        kubectl get secret es7-es-http-certs-public -o json | \
            jq -r '.data["ca.crt"] | @base64d' > es7-ca.crt
        keytool -importcert -file es7-ca.crt -alias es7-ca \
            -keystore store-es7 -storetype JKS -storepass changeit
        
        kubectl get secret es74h4-es-http-certs-public -o json | \
            jq -r '.data["ca.crt"] | @base64d' > es74h4-ca.crt
        keytool -importcert -file es74h4-ca.crt -alias es74h4-ca \
            -keystore store-es74h4 -storetype JKS -storepass changeit

     Place the files ``store-es7`` and ``store-es74h4`` into the
     ``migration-configs`` directory.

 26. Make a secret with all the migration configs and trust stores in
     it::

       kubectl create secret generic migration-configs \
           --from-file=migration-configs

 27. Make a secret to store the Play overrides configuration, for
     which the code of the migration tool specifically reaches
     out. `This file
     <https://github.com/TheHive-Project/TheHive/blob/7d6d55d6844df96e59769b2ca46dae5627977664/thehive/conf/play/reference-overrides.conf>`_
     is not included in TheHive Docker image. ::

       mkdir play-overrides
       cat > play-overrides/reference-overrides.conf <<BAZINGA
       # HTTP filters
        play.filters {
          # name of cookie in which the CSRF token is transmitted to client
          csrf.cookie.name = THEHIVE-XSRF-TOKEN
          # name of header in which the client should send CSRD token
          csrf.header.name = X-THEHIVE-XSRF-TOKEN

          enabled = [
          ]
        }

        play.http.parser.maxDiskBuffer = 128MB
        play.http.parser.maxMemoryBuffer = 256kB


        # Register module for dependency injection
        play.modules.enabled += org.thp.thehive.TheHiveModule

        play.http.session.cookieName = THEHIVE-SESSION

        play.server.provider = org.thp.thehive.CustomAkkaHttpServerProvider

        play.server.http.idleTimeout = 10 minutes

        akka.actor {
          serializers {
            stream = "org.thp.thehive.services.StreamSerializer"
            notification = "org.thp.thehive.services.notification.NotificationSerializer"
            //thehive-schema-updater = "org.thp.thehive.models.SchemaUpdaterSerializer"
            flow = "org.thp.thehive.services.FlowSerializer"
            integrity = "org.thp.thehive.services.IntegrityCheckSerializer"
            caseNumber = "org.thp.thehive.services.CaseNumberSerializer"
          }

          serialization-bindings {
            "org.thp.thehive.services.StreamMessage" = stream
            "org.thp.thehive.services.notification.NotificationMessage" = notification
            //"org.thp.thehive.models.SchemaUpdaterMessage" = thehive-schema-updater
            "org.thp.thehive.services.FlowMessage" = flow
            "org.thp.thehive.services.IntegrityCheckMessage" = integrity
            "org.thp.thehive.services.CaseNumberActor$Message" = caseNumber
          }
        }
        BAZINGA
        kubectl create secret generic play-overrides \
            --from-file=play-overrides

Actually run the migration script
.................................

 28. Write this into ``migrate-job.yaml``::

        apiVersion: batch/v1
        kind: Job
        metadata:
          namespace: hivemig
          name: migration-3to4
        spec:
          completions: 1
          backoffLimit: 1
          template:
            spec:
              restartPolicy: Never
              volumes:
                - name: configs
                  secret:
                    secretName: migration-configs
                - name: play-overrides
                  secret:
                    secretName: play-overrides
              containers:
                - name: migrate
                  image: thehiveproject/thehive4:4.1.7-1
                  volumeMounts:
                    - name: configs
                      mountPath: /configs
                    - name: play-overrides
                      mountPath: /opt/thehive/config/play
                  args:
                    - "migrate"
                    - "--"
                    - "--input"
                    - "/configs/hive3.conf"
                    - "--output"
                    - "/configs/hive4.conf"
                    - "--drop-database"
                    - "--main-organisation"
                    - "example.org"

 29. Now ``kubectl apply -f migrate-job.yaml``.
 30. Follow its logs. ::
       
       MIG_POD=$(kubectl get -o json pod | jq -r '.items[].metadata.name | select(startswith("migration-3to4"))')

What now?
---------

Now you have a new TheHive4 instance with your stuff in it. Do
new-thehive4-instance things, like changing the password of
admin@thehive.local post-haste. Refer back to TheHive4 documentation
because you are now more or less back on the beaten path.

What's missing?
---------------

The ScyllaDB set up here does not compel authentication, nor secure
its connections with TLS.

For both Scylla (or Cassandra, if you use that instead) and
Elasticsearch, there are day-2 considerations such as logging,
monitoring, backup, and restoration to deal with. You may need a
long-lived MinIO instance to snap your Elasticsearch cluster into: I
tried a ReadWriteMany PersistentVolume, and it didn't work right. I
think I got one per Elasticsearch node or something.
