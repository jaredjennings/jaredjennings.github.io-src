OpenWRT monitoring, part 4
##########################
:date: 2022-12-01 00:51
:author: jaredj
:category: Home IT

The second router
-----------------

I've added my second router to the monitoring scheme. This consisted in:

 1. installing the packages I've listed before;
 2. writing the same config files on the second router, but with its
    name in them instead;
 3. creating another mosquitto user and password. Take note that when
    you use the ``-c`` switch to ``mosquitto_passwd``, it wipes out
    any other passwords you may have written in the file. Also it
    seems you have to restart ``mosquitto`` for it to see changes in
    this file.
 4. making sure this router can talk to my MQTT broker, what with
    VLANs, addresses, firewall rules, and the like.

Collecting
----------

To actually write down all this stuff, I've created another jail on my
host called ``collectd``.

Plugins
=======

The ``collectd5`` package available from the FreeBSD package servers
doesn't have the MQTT plugin nor the rrdtool plugin. So I have to
build a custom package for it.

I have a ``portbuild`` jail, which has a copy of the ports checked out
in ``/usr/ports`` using ``portsnap``. Going in
``/usr/ports/net-mgmt/collectd5`` and typing ``make config``, I can
turn on MQTT support. Now I type ``make package``, and when it tries
to build the ports that the collectd5 port now depends on because of
my decisions, I type Ctrl-C and ``pkg install`` the
dependencies. These are ``mosquitto``, ``rrdtool``, ``liboping``, and
one or two others I don't remember. There's probably a better way to
do this, but this worked.

After ``make package`` finishes, the ``work`` subdirectory contains
the package. Copying this over into root's home in the ``collectd``
jail, I can ``sudo iocage pkg collectd install
/root/collectd*pkg``. This pulls in all the packages that provide the
dependencies my custom collectd package has.

Configuration
=============

Opening up the ``/usr/local/etc/collectd.conf``, I see it has a lot of
commented defaults to start from. I disable all the existing plugins,
and enable mqtt, rrdtool, and unixsock. (A cursory reading of the
`rrdtool plugin documentation`_ on the collectd wiki indicates I may
need to tell collectd to flush data out before drawing charts.)

.. _`rrdtool plugin documentation`: https://collectd.org/wiki/index.php/Inside_the_RRDtool_plugin

ZFS
===

That same page indicates that rrdtool databases get a lot of small
writes, so I want to turn down the ZFS data block size where those
will happen. I find the dataset ``.../iocage/jails/collectd/root``
corresponding to the jail's filesystem, create ``var`` and ``var/db``
sub-filesystems, and ``zfs set recordsize=4K .../var/db``. For SQL
databases, 8K is frequently recommended, but this page says there are
dozens of bytes that get written to places in the file. Maybe the
caching that's done makes this unnecessary; I don't know for sure.

Oops, there was probably stuff in ``/var/db``, so I ``zfs set
mountpoint=.../db2 .../var/db``, go in the jail, ``mv /var/db/*
/var/db2/``, and then put the mountpoint back.

It would be tidier to set the recordsize only on the rrdtool
databases, but those are two directory levels down and gosh c'mon.

Starting it up
==============

I've told my collectd mqtt plugin to connect to my MQTT host, and
listen to topic ``collectd/#`` (that means any topic whose name starts
with "collectd/"). Now I can start collectd, and presto change-o! I've
got rrd files.

Shutting it down
================

Oh! I've got rrd files for each station MAC address, as I foresaw an
article or two ago. That's going to be too many. Shut it down!

I suppose the script I interpose is going to have to (1) postprocess
all the per-station data; *and* (2) pass all the rest of the data
through; *and* (3) publish to a topic that doesn't start with
"collectd/". Then I'll have to tell collectd to listen to that
post-processed topic and write those things down in the rrd database
files.

Postprocessing script
---------------------

I don't see MQTT clients for Common Lisp nor Chicken Scheme, my
parenthesis-laden languages of choice. This would be an opportunity to
contribute; but I don't know anything about MQTT already. Maybe later.

Why don't I feel like doing it in Python? Wonder what other languages
have clients already... <https://mqtt.org/software/>. Rust does, too,
at crates.io. I'm in a little of a Lua mood since writing that input
plugin in Lua. - Oo, maybe this is an opportunity to try Fennel.


