Somebodyoughta: Firefox Sync 1.5 + OpenShift Quickstart
#######################################################
:date: 2014-10-11 20:16
:author: jaredj
:category: Cloud
:tags: somebodyoughta
:slug: firefox-sync-1-5-openshift-quickstart
:status: published

`Firefox Sync
1.5 <https://docs.services.mozilla.com/howtos/run-sync-1.5.html>`__, the
Sync version behind Firefox 29 and later, helps you share tabs and
preferences across Firefox instances on multiple devices. It appears to
be a WSGI application.

OpenShift has a Python cartridge that can run WSGI applications.

Hooking the two up would be a matter of writing OpenShift build scripts
that call the right Sync build scripts, and providing configuration to
hook Sync up to some database. Seems pretty easy.

Somebodyoughta do it. If I do it before you do, I'll let you know right
here.
