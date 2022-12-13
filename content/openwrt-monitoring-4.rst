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

Ignoring some
-------------

I found that collectd has filter chains, where you can tell it to
ignore some data. I added the following directives to my
``collectd.conf`` on the central collectd server::

  LoadPlugin match_regex
  
  <Chain "PreCache">
    # Ignore stats emitted for each WiFi association: MAC addresses can
    # be randomized and we should not sprout a gazillion
    # per-MAC-address rrd databases. These will be grokked by a
    # summarizer script which will place its results on another MQTT
    # topic.
    <Rule "ignore_iw_assoc">
      <Match "regex">
        Plugin "^iw_assoc$"
      </Match>
      <Target "stop">
      </Target>
    </Rule>
  </Chain>

I found that the plugin is split from the plugin instance using the
first dash, so I had to change my emitted plugin name from "iw-assoc"
to "iw_assoc." I've edited the earlier post to reflect this.

Postprocessing script
---------------------

I don't see MQTT clients for Common Lisp nor Chicken Scheme, my
parenthesis-laden languages of choice. This would be an opportunity to
contribute; but I don't know anything about MQTT already. Maybe later.

Why don't I feel like doing it in Python? Wonder what other languages
have clients already... <https://mqtt.org/software/>. Rust does, too,
at crates.io. I'm in a little of a Lua mood since writing that input
plugin in Lua. - Oo, maybe this is an opportunity to try Fennel. ::

  luarocks54 install fennel

That worked. OK, ::

  luarocks54 install luamqtt

That needed git installed. ::

  exit
  sudo iocage pkg collectd install git
  # type "y", without being able to see the prompt
  sudo iocage console collectd
  luarocks54 install luamqtt

That installed luasocket, even though I thought I had installed it
with `pkg`. Whatever. ::

  fennel
  [...]
  
  >> (local x (require "mqtt"))
  nil
  >> x
  {:_VERSION "3.4.3"
   :client #<function: 0x800afa890>
   :get_ioloop #<function: 0x800af9630>
   :run_ioloop #<function: 0x800b21240>
   :run_sync #<function: 0x800a8dfe0>
   :v311 4
   :v50 5}
  >>

OK, so here's Fennel beating the pants off Lua at step one. The Lua
REPL doesn't print the value it evaluates, and you can't even just
``print(x)`` if x is a table. I guess that's just a read-eval loop,
not a read-eval-print loop.

Run code every so often
=======================

The `luamqtt documentation`_ was enough to help me write a client in
Fennel that subscribes and prints messages. Then I realized I don't
want to publish a message upon reception of each message, I want to
absorb information and publish it on a time interval. Poking around
some, I found that the ioloop provided by luamqtt is rudimentary, and
while it's easy to get my own function in there and being called, it's
not as easy to make it only run so often, without taking 100% CPU
polling for whether that time has arrived yet.

.. _`luamqtt documentation`: https://xhaskx.github.io/luamqtt/index.html

`In the luamqtt source`_, but not in the documentation, there is an
example that uses `copas`, another Lua module, to do non-MQTT work in
the same event loop. ``luarocks54 install copas``!

.. _`In the luamqtt source`: https://github.com/xHasKx/luamqtt/blob/master/examples/copas-example.lua

Script!
=======

::

  #!/usr/local/bin/fennel
  ; exec /usr/local/bin/fennel $0
  ;; why is the above exec necessary?? the shebang should do it

  ;; thanks https://xhaskx.github.io/luamqtt/examples/simple.lua.html
  ;; thanks https://github.com/xHasKx/luamqtt/blob/master/examples/copas-example.lua

  (local mqtt (require :mqtt))
  (local mqtt_ioloop (require :mqtt.ioloop))
  (local copas (require :copas))
  (local posix (require :posix))

  (local connection-details {:uri "mqtt.agrue.info"
                            :username "collectd-iwassocfilter"
                            :password "ofaUtrrm65V8OFZuNpYs3ZuU"
                            :clean true})

  (local topic "collectd/#")

  ;; following the parse_identifier definition in collectd source:
  ;; https://github.com/collectd/collectd/blob/dfd034032b7c7c8f821774715c0723c42cefd332/src/utils/common/common.c#L972
  ;;
  ;; vl is short for value_list_t, a struct containing fields for
  ;; hostname, plugin, type, plugin instance, and type instance
  (fn topic-to-vl [topic]
    (let [[_ hostname pluginstuff typestuff]
          (icollect [x (string.gmatch topic "([^/]+)")] x)
          (plugin plugin-instance)
          (string.match pluginstuff "([^-]+)-?(.*)")
          (type type-instance)
          (string.match typestuff "([^-]+)-?(.*)")
          ret {: hostname : plugin : type}]
      (if (not= plugin-instance "")
          (set ret.plugin-instance plugin-instance))
      (if (not= type-instance "")
          (set ret.type-instance type-instance))
      ret))

  (fn vl-to-topic [vl]
    (string.format "collectd/%s/%s%s/%s%s"
                   vl.hostname vl.plugin
                   (if (or (not vl.plugin-instance)
                           (= vl.plugin-instance ""))
                       ""
                       (.. "-" vl.plugin-instance))
                   vl.type
                   (if (or (not vl.type-instance)
                           (= vl.type-instance ""))
                       ""
                       (.. "-" vl.type-instance))))

  (fn payload-to-values [payload]
    (let [[time & vals]
          (icollect [x (string.gmatch payload "([^:\000]+)")] x)
          numbers (icollect [_ v (ipairs vals)] (tonumber v))]
      {: time : numbers}))

  (fn zip [...]
    "(zip [1 2 3 4] [5 6 7]) => [[1 5] [2 6] [3 7]]"
    (let [nargs (select :# ...)
          args (fcollect [i 1 nargs] (select i ...))
          lengths (icollect [_ v (ipairs args)] (length v))
          minimum-length (math.min (table.unpack lengths))]
      (fcollect [n 1 minimum-length]
        (icollect [i v (ipairs args)] (. v n)))))

  (fn calc-over-window [window]
    "Do aggregate calculations over all measurements in window. Return a table of messages to publish, [{topic [time val1...]}...]."
    (let [
          ;; if time is nil, no worries: we have no values to aggregate,
          ;; and we will have 0 places to write time.
          time (tonumber (?. window 1 :time))
          groups {}
          messages {}]
      (print (length window) "measurements in window")
      ;; gather values of interest
      (each [i info (ipairs window)]
        (when (and (not info.type-instance) ; e.g. skip -avg
                   (= info.plugin "iw_assoc"))
          ;; strip off station mac, leaving interface
          (set info.plugin-instance
               (string.match info.plugin-instance
                             "(.*)-STA-.*"))
          (let [group (vl-to-topic info)]
            (if (not (?. groups group)) (tset groups group {}))
            (table.insert (. groups group) info))))
      (each [groupname infos (pairs groups)]
        (print "group" groupname "has" (length infos) "infos"))
      ;; now aggregate those
      (each [_ funcinfo
             (ipairs [[math.min     #(set $1.type-instance "min")]
                      [math.max     #(set $1.type-instance "max")]])]
        (let [[func mutate-typestuff] funcinfo]
          (each [group infos (pairs groups)]
            (let [agginfo {}
                  allnumbers (icollect [_ info (ipairs infos)]
                               (. info :numbers))
                  ;; each :numbers can contain multiples (e.g. rx, tx)
                  eachset (zip (table.unpack allnumbers))]
              (each [k v (pairs (. infos 1))]
                (when (and (not= k :numbers) (not= k :time))
                  (tset agginfo k v)))
              ;; change plugin name to our own: collectd is configured to
              ;; ignore unaggregated iw_assoc plugin
              (set agginfo.plugin "iw_assoc_agg")
              (mutate-typestuff agginfo)
              (let [aggtopic (vl-to-topic agginfo)]
                (tset messages aggtopic
                      (icollect [_ es (ipairs eachset)]
                        (func (table.unpack es)))))))))
      (let [nmessages (accumulate [x 0 k v (pairs messages)] (+ x 1))]
        (print "we have" nmessages "messages this time"))
      ;; prepend the time - for every aggregate measurement, write the
      ;; same moment, the one at the beginning of this window
      (each [topic extremum (pairs messages)]
        (table.insert extremum 1 time))
      messages))


  (let [client (mqtt.client connection-details)
        window [[]]
        subscribed (fn [suback]
                     (print "subscribed: " suback))
        connected (fn [connack]
                    (if (= connack.rc 0)
                      (do (print "connected: " connack)
                          (assert (client:subscribe {:topic topic
                                                     :qos 1
                                                     :callback subscribed})))
                      (print "connection to broker failed: "
                             (connack:reason_string)
                             connack)))
        message-received (fn [msg]
                           (assert (client:acknowledge msg))
                           (when (string.match msg.topic "^collectd/")
                             (let [info (topic-to-vl msg.topic)]
                               (when (= info.plugin "iw_assoc")
                                 (when (not (. window 2))
                                   (table.insert window {}))
                                 (let [add (payload-to-values msg.payload)]
                                   (each [k v (pairs add)]
                                     (tset info k v)))
                                 (table.insert (. window 2) info)))))
        error-happened (fn [err]
                         (print "MQTT client error: " err))
        ]
    (client:on {:connect connected
                :message message-received
                :error error-happened})
    (copas.addthread
     (fn []
       (let [ioloop (mqtt_ioloop.create {:sleep 0.01
                                         :sleep_function copas.sleep})]
         (ioloop:add client)
         (ioloop:run_until_clients))))
    (copas.addthread
     (fn []
       (local fennel (require :fennel))
       (while true
         (copas.sleep 10)
         (let [aggmessages (calc-over-window (. window 1))]
           (each [topic extremum (pairs aggmessages)]
             (let [payload (table.concat extremum ":")]
               (client:publish {: topic : payload :qos 1}))))
         (table.remove window 1))))
    (copas.loop)
    (print "done"))

Opinions
========

Multiple-value return feels easier than in Scheme, and is used more
often. The table as primary data structure feels stilted; I guess this
is because it makes it matter a great deal what kind of brackets I
use, and I have to pick between ``icollect``, ``collect``,
``accumulate``, and ``fcollect``. No ``apply`` or ``map`` per se. I'm
disappointed that iterators and generators aren't coroutines like in
Python. Table manipulation is mostly imperative and destructive, which
makes me use ``each`` loops in some places I'd normally like to use
``map``. Destructuring is nice. Varargs don't seem very nice. It was
mostly easy to read documentation about Lua and figure out how it
would apply to Fennel.

I don't know a great deal more than I did when beginning about exactly
how the abstractions work. That's because they didn't leak very much,
which is really great! I think I like Fennel better than Lua, and I
really liked how easy it was to get started. Tiny downloads, few
concepts. But I'm still going to keep looking around.


