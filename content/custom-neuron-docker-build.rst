Building your own Cortex neuron in a Docker image
#################################################
:date: 2021-10-04 13:45
:author: jaredj
:category: Security
:tags: cortex, docker, cloud, kubernetes

Neurons
-------

In the context of computer security incident response using TheHive
and Cortex, `neurons` are pieces of software invoked by Cortex which
perform the analysis (`analyzers`) of some observables producing a
report, or use the observables to in some way respond (`responders`)
to a threat.

As an example, the VirusTotal analyzer can take a hash observable,
send a web request to VirusTotal to search for it, and return the list
of engines which detected a threat in the file with that hash, as well
as the count of detections, which is used to give a colored tag to the
observable.

Another example is the DNS-RPZ responder. It can take a [DNS] domain
observable, and feed it to a DNS blackhole server configured using
DNS-RPZ, such that anyone in the organization who tries to look up
that DNS name will be directed aside from the real (malicious) site.

Cortex is at this point in history able to kick these off (`run a
job`) in two ways: by executing them as subprocesses (with the
``process`` JobRunner, or ``fork-join-executor``), or by communicating
with a Docker daemon via Unix socket to run them inside containers
(the ``docker`` JobRunner). No one has yet contradicted me when I
guessed that calling analyzers and responders collectively as
`neurons` came at the same time as the ability to run them as
containers. In some code they may also be called `workers.`

(A third way of running jobs, using Kubernetes, was pull-requested in
https://github.com/TheHive-Project/Cortex/pull/349 in March 2021, but
as of October 2021 has not been merged.)


Custom analyzers with the subprocess job runner
-----------------------------------------------

Outside of Docker, Cortex has configuration items ``analyzer.path``
and ``responder.path`` where you list directories where Cortex should
look for analyzers and responders. Each analyzer or responder consists
of a directory inside one of those path entries, with one or more
flavor JSON files, one or more executable files, and any other needed
files. So, for example, if Cortex is configured to have ``/dir1`` in
its ``analyzer.path``, a ``dhcp_info`` analyzer would be arranged
therein like so::

    -- /dir1
    |
    \-- dhcp_info
         |
         |-- dhcp_info.json
         \-- dhcp_info_executable

where ``dhcp_info.json`` names ``dhcp_info_executable`` as the
``command``::

    {
        "name": "dhcp_info",
        "command": "dhcp_info/dhcp_info_executable",
        [...]
    }

(Note that the pathname of the command is relative not to the
analyzer's directory ``dhcp_info``, but to ``/dir1``.)


Cortex-Analyzers
----------------

Any analyzer or responder that didn't already exist as part of
https://github.com/TheHive-Project/Cortex-Analyzers/, and that
therefore you had to write, you are urged to pull-request into that
repository (which was clearly named before responders had been
conceived). Once it is merged, anyone who is running Cortex not using
Docker, and is following the official directions, will obtain it when
installing Cortex and be able to use it.


Neuralizing
-----------

But installing a real Cortex with real files on a real server is so
passé. Don't you want to be using Docker? It's much easier to set
up. When Cortex is using the Docker job runner, you don't have to
worry about installing a bunch of Python module dependencies on your
server - they just magically come in the container with the analyzer!
Instead of a list of directories containing json files and
executables, Cortex is configured with a list of URLs to JSON files
with info about the `neurons` it has, including the container images
to pull and run.

As long as the analyzers and responders you care about are part of the
official build, everything works quite nicely for you. But if you need
a newer version of an analyzer, or one that has not yet been
integrated into the `Cortex-Analyzers` repository, what then? (At this
writing there are 54 open pull requests against Cortex-Analyzers. You
may know I am not neutral on this issue, because three of those are
from me.)

Most of the analyzers were not written by people who at the time
expected their code would be built into a container. How is it made
so? The neuron images are uploaded to
https://hub.docker.com/u/cortexneurons by the
`cortex-neurons-builder`_, and cataloged into the JSON file hosted at
(e.g.) https://download.thehive-project.org/analyzers.json. That file
is allegedly a `concatenation`_ of all the JSON flavor files into one
JSON array; but there seems to be a ``dockerImage`` value added in
there, somehow.

.. _`cortex-neurons-builder`: https://github.com/TheHive-Project/cortex-neurons-builder
.. _`concatenation`:
   https://github.com/TheHive-Project/CortexDocs/blob/5fdc930feb2d5a9f95fcabd7d96dccedae62d993/admin/cortex3.md


Custom neurons
--------------

So how to include your own neurons in a Cortex instance using Docker
(or Kubernetes, where the job runner uses the same container images)?

Officially, you could run your own `cortex-neurons-builder`. It is
open-source, after all. This is how you would automate the build. But
if you don't build your code very often, here's how
`cortex-neurons-builder` does it, in English:

 1. Add a Dockerfile to your analyzer/responder. Make it say this::

        FROM python:3
        WORKDIR /worker
        COPY . {worker_name}
        RUN test ! -e {worker_name}/requirements.txt || pip install --no-cache-dir -r {worker_name}/requirements.txt
        ENTRYPOINT {command}
        
    where ``{worker_name}`` is the name of the subdirectory your
    analyzer/responder code is in (``dhcp_info`` from our example
    above), and ``{command}`` is the value of ``command`` from the
    flavor JSON file.
 2. This step number is reserved in case I find out the metadata
    included at `registry.py line 47
    <https://github.com/TheHive-Project/cortex-neurons-builder/blob/fe8c39333c3ebf52db8ce6a0ea83878998774bba/registry.py#L47>`_
    are absolutely necessary.
 3. Build this using `buildah <https://buildah.io>`_ or Docker. Push
    this to your own local container registry. (`Insecure local
    unauthenticated registry <cortex-on-kubernetes.html>`_ in section
    2 of that link.)
 4. Collect the flavor JSON files. For each flavor, add a
    ``dockerImage`` value that points to the image inside your own
    registry.
 5. Place the aggregate JSON file somewhere in a filesystem visible to
    your Cortex instance.
 6. Add ``file:///my/analyzer/list.json`` to the ``analyzer.urls``
    list in your Cortex configuration.
 7. Do likewise for responders; the list of those is configured in the
    ``responder.urls`` list in Cortex's configuration.
 8. You may need one image per flavor, not per analyzer/responder; if some
    of your analyzers/responders have more than one flavor, that's
    an exercise for the reader. 


Totally custom neurons
----------------------

As a "Day-2" task, you should build a complete set of your own
neurons, just like you should have built your own container images for
all the other software you run... You did do that, right?
