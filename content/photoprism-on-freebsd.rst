Photoprism on FreeBSD 13.1
##########################
:date: 2022-05-26 21:51
:author: jaredj
:category: Home IT


First try
---------

Photoprism depends on TensorFlow. In May 2022, the py38-tensorflow
package `does not build
<https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=259620>`_. Also
it's pretty old.

 1. Create a jail. Java needs proc and /dev/fd::
        
        iocage create -r 13.1-RELEASE -n portbuild ip4_addr='[...]'
        iocage set mount_procfs=1 mount_fdesc_fs=1 portbuild
 
 2. Start the jail and go into it::
        
        iocage start portbuild
        iocage console portbuild
 
 3. Install prerequisites for Photoprism build::
        
        pkg install ffmpeg p5-Image-ExifTool bash gmake go npm wget python
 
 4. According to the bug linked above, TensorFlow 1.15 is pretty old. Prepare to build 2.1. The ``bazel`` package is way too new to do this; you need ``bazel029``. My clue there was that the build errors out on a switch called `incompatible_no_support_tools_in_action_inputs <https://docs.bazel.build/versions/0.25.0/skylark/backward-compatibility.html#disallow-tools-in-action-inputs>`_, which was added in version 0.25.0 and was to be temporary. ::
        
        pkg install bazel029
        pkg install bash swig py38-cython pcre snappy lmdb sqlite3 icu jsoncpp nsync protobuf protobuf-c re2 giflib png grpc curl google-cloud-cpp117 flatbuffers double-conversion py38-{grpcio-tools,absl,astor,gast,numpy,google-pasta,protobuf,six,termcolor,grpcio,keras,wrapt,wheel}
        fetch -o tensorflow-2.1-port.shar 'https://bugs.freebsd.org/bugzilla/attachment.cgi?id=229235'
        perl -pe 's/\r\n/\n/g' tensorflow-2.1-port.shar > tensorflow-2.1-port.shar.nlfix
        sh tensorflow-2.1-port.shar.nlfix
        cd py-tensorflow
        fetch -o files/patch-bug-259620-att-232155 'https://bugs.freebsd.org/bugzilla/attachment.cgi?id=232155'
        fetch -o files/patch-error_message 'https://bugs.freebsd.org/bugzilla/attachment.cgi?id=234250'
 
 5. Build something::
        
        make config
        # pick yes for the cpu optimizations
        make package
 
 6. Wait about an hour (on my machine).
 7. It still doesn't build. Errors like this::
 
        tensorflow/python/lib/core/bfloat16.cc:648:8: error: no matching function for call to object of type '(lambda at tensorflow/python/lib/core/bfloat16.cc:607:25)'
          if (!register_ufunc("less_equal", CompareUFunc<Bfloat16LeFunctor>,
               ^~~~~~~~~~~~~~
        tensorflow/python/lib/core/bfloat16.cc:607:25: note: candidate function not viable: no overload of 'CompareUFunc' matching 'PyUFuncGenericFunction' (aka 'void (*)(char **, const long *, const long *, void *)') for 2nd argument
          auto register_ufunc = [&](const char* name, PyUFuncGenericFunction fn,
                                ^
 8. Sign up to bugs.freebsd.org and tell folks about it because it's one step past what is already written.

Updates as events warrant. (Surely OP will deliver!)

Second try
----------

I tried making a Linux jail. I managed to get Debian 11.3 up following
some directions I don't remember now. I think I created an empty jail
with iocage, then used debootstrap (which is installable as a FreeBSD
package) to put all the files into it. Upgrade to 11.5 worked ok. It
seemed like a good idea to set the ``linprocfs_mounted`` option on the
jail. There was no photoprism package in the apt repository for
bullseye. I updated it to the latest Sid, and while it ran bash fine,
systemctl didn't work. (Go figure.) It said systemd-whatnot wasn't pid
1 and barfed. I destroyed the jail. I think Devuan would be the next
best step along this line. Or if I could ... hmm. I don't really need
a distro for Photoprism to run on, unless there's a nice package for
me to install. If I've got to build Photoprism, it would be better for
what I run in the jail to be more like ... the contents of a container
image. Such an image might assume a newer kernel just like Sid did
though.

Third try
---------

Ok py-tensorflow was a complete red herring - that port/package is for
getting TensorFlow accessible from Python, and we really need it
accessible from C. (Photoprism is in C#, but it links against the C
library. I think.)

Fired up the photoprism jail, updated the ports tree, ran ``make
clean`` at the top.

Somehow I have not yet mentioned the `Photoprism FreeBSD
port`_. That's kind of important.

.. _`Photoprism FreeBSD port`: https://github.com/huo-ju/photoprism-freebsd-port

It says, "This port depends on science/libtensorflow1." I don't see a
package for that. So that's the port I need to build a package for,
first. ... As soon as my ``make clean`` finishes. It's moved on from
"astro" to "audio". That could take a while... ok I gave up during
"databases," went straight to science/libtensorflow1, checked its deps
in its Makefile, pkg installed them (because I don't want to build the
hundreds of ports in the transitive dependency tree), and set to
``make package`` in science/libtensorflow1. And the port is marked
broken because it fetches during the build stage. OK, comment out the
``BROKEN`` declaration and blunder ahead. No GPU acceleration just
yet - I want this build as simple as possible.

OK, more transitive dependencies to install - ``py39-cython-devel``,
eh that's about it. There are some Google libraries I could fetch, but
it's not easy to figure out which ones. Right? That's a bit of a
shame - they are transitive dependencies, and they are ports. So to
figure out which packages to install, first I'd have to list them all,
then figure out a correspondence to package names. I don't see tools
that do that laying about. Hope I'm wrong there.

And Bazel is off and building. ... and::

  ERROR: /usr/ports/science/libtensorflow1/work-default/tensorflow-1.15.5/tensorflow/core/BUILD:2724:1: ProtoCompile tensorflow/core/framework/op_def.pb.h failed (Illegal instruction): protoc failed: error executing command
    (cd /usr/ports/science/libtensorflow1/work-default/bazel_out/98e92f9393bc83ca8c28c921fe93f245/execroot/org_tensorflow && \
    exec env - \
      PATH=/usr/ports/science/libtensorflow1/work-default/.bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin:/root/bin \
      PYTHON_BIN_PATH=/usr/local/bin/python3.9 \
      PYTHON_LIB_PATH=/usr/local/lib/python3.9/site-packages \
      TF2_BEHAVIOR=0 \
      TF_CONFIGURE_IOS=0 \
    bazel-out/host/bin/external/com_google_protobuf/protoc '--cpp_out=bazel-out/freebsd-opt/bin' -I. -I. -Iexternal/com_google_protobuf/src -Ibazel-out/freebsd-opt/bin/external/com_google_protobuf/src -Iexternal/com_google_protobuf/src -Ibazel-out/freebsd-opt/bin/external/com_google_protobuf/src tensorflow/core/framework/op_def.proto)



