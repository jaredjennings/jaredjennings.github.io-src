Photoprism on FreeBSD 13.1
##########################
:date: 2022-05-26 21:51
:author: jaredj
:category: Projects

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
