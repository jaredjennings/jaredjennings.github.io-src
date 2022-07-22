Running the latest iocage on FreeBSD with pex
#############################################
:date: 2021-05-04 00:01
:author: jaredj
:category: Home IT
:tags: iocage, jails, freebsd, pex

While trying to move iocage jails from one machine to another, I found
that iocage import tries to read its entire input into RAM, in the
version of iocage I had installed via pkg(1). Furthermore, I `found
<https://github.com/iocage/iocage/issues/1086#issuecomment-809902293>`_
that the problem had been fixed already, but that no iocage release
had been made that contained the fix, for more than a year. So no one
has packaged a version of iocage that contains the fix.

I didn't really want to install the latest iocage and scatter files
over my system: not least because if it's no good, I want to be able
to remove it easily.

::

   git clone https://github.com/iocage/iocage
   cd iocage
   python3 -m venv ve
   source ve/bin/activate
   pip install -r requirements.txt
   python3 setup.py bdist_wheel
   # it will bomb out because build/.../wheel/iocage_lib does not exist
   mkdir # build/.../wheel
   mkdir # build/.../wheel/iocage_lib
   mkdir # build/.../wheel/iocage_cli
   # that was a kluge within a kluge
   deactivate
   python3 -m venv pexve
   source pexve/bin/activate
   pip install --upgrade pip
   pip install pex
   pex -v -m iocage_cli:cli -o iocage-sac \
       -r requirements.txt \
       ./dist/iocage_cli-1.2-py3-none-any.whl \
       ./dist/iocage_lib-1.2-py3-none-any.whl

The result is a single file, iocage-sac, which contains all of iocage
and its dependencies, but not Python. I placed it in /usr/local/bin.

Not having an installed copy of iocage means I don't have the rc
script installed, so my jails don't start on boot. That would be a
small matter of scripting, but I haven't bothered with it yet.
