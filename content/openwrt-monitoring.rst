Monitoring OpenWRT
##################
:date: 2022-11-25 00:56
:author: jaredj
:category: Home IT

Context
-------

I've got two OpenWRT routers. Each provides two wireless networks, one
at 2.4GHz and one at 5GHz, all four under the same SSID. Fast
transition (FT, roaming, 802.1r) is configured. The networks are
bridged together, and actually routed by only one of the routers. I've
left LuCI, OpenWRT's web UI, behind long ago: I don't like clicking
buttons, and I do like editing text files. I would like to minimize
the number of millions (!) of lines of code I run. I've been burned by
company-supported open source software going freemium.

Problem
-------

Devices fall off the WiFi occasionally, and no one knows why. What's
going on? Is the roaming working? Isn't 5GHz wifi supposed to be
faster? I've tried keep the routers out of reach of children, but in
reach of power and Ethernet; is their placement any good for signal
strength? I got on the router via ssh one night when someone had just
fallen off the WiFi and it appeared to be very busy - hostapd and
dnsmasq taking up all the CPU - but only for a moment.

Solution
--------

Collect and monitor metrics from the routers.

But how? I've looked at snmpd, collectd, statsd, mrtg, cacti,
graphite, grafana, influxdb, rrdtool, drraw, and others. Here's what
I've learned:

snmpd achieves small size and simplicity through dependency on the
centrally coordinated OID namespace. I'm not entirely certain how to
make it gather wireless station association data, nor how I would
configure it normally. OpenWRT adds another layer on top of that with
its configuration system; the documentation appears to be sufficient
for people experienced with snmpd, but not for me. I've had enough
mental blocks trying to get it working to give up on it.

mrtg was originally written to talk SNMP, but can execute scripts to
get metrics. rrdtool is nicer than mrtg in almost every way. drraw is
dead. Cacti is made in PHP, and has a company behind it. Graphite was
"begun in 2006 at Orbitz;" perhaps being old it is smaller than
Grafana, but it's a bit trendy. InfluxDB and Grafana are the current
hotness but I don't want that. Maybe I'd learn more about them if I
thought I could use them at work, but at this point we pay other
people to integrate such things and sell them to us as
appliances. statsd is too trendy.

collectd is written in C and uses dynamically loaded modules to
collect metrics. This makes it old, small, fast, and flexible. It's
packaged in OpenWRT. It works with rrdtool, but I don't have
persistent storage on my router and I like it that way. collectd can
send metrics over the network, using its own protocol or MQTT. I've
been wanting to do things with MQTT.

The story so far
----------------

Now! The part where I write down what I've done, because it's getting
too complicated to remember all of it, it's not directly manageable
enough where I can write it down in Puppet or Ansible or Adams, and I
despair that my requirements would change by the next time I needed
what I'd written, so I'll do it in prose so there.

collectd
========

Install the following packages on the router using ``opkg``::

  collectd
  collectd-mod-conntrack
  collectd-mod-cpu
  collectd-mod-dhcpleases
  collectd-mod-interface
  collectd-mod-iptables
  collectd-mod-iwinfo
  collectd-mod-load
  collectd-mod-lua
  collectd-mod-memory
  collectd-mod-mqtt
  collectd-mod-network
  collectd-mod-ntpd
  collectd-mod-processes
  collectd-mod-uptime
  collectd-mod-wireless

`Configure collectd`_ by writing ``/etc/collectd.conf``::

  BaseDir "/var/lib/collectd"
  PIDFile "/var/run/collectd.pid"
  Interval 10
  ReadThreads 2

  LoadPlugin cpu
  LoadPlugin interface
  LoadPlugin load
  LoadPlugin memory
  LoadPlugin processes
  LoadPlugin uptime
  LoadPlugin iwinfo
  LoadPlugin wireless
  LoadPlugin mqtt

  <Plugin interface>
    IgnoreSelected false
    Interface br-dmz
    Interface br-guest
    Interface br-inside
    Interface br-mgmt
    Interface eth0.87
    Interface 6in4-henet
  </Plugin>

  <Plugin processes>
    Process "dnsmasq"
    Process "hostapd"
  </Plugin>

  <Plugin mqtt>
    <Publish "mqtt">
      Host "my-mqtt-host.mydomain.example.com"
      Prefix "collectd"
      User "router-username"
      Password "super-secure-password"
    </Publish>
  </Plugin>

.. _`Configure collectd`: https://openwrt.org/docs/guide-user/perf_and_log/statistic.collectd?s[]=collectd

Start a jail to run the MQTT broker::

  sudo iocage create -r 13.1-RELEASE -n mqtt \
    ip4_addr='mydmz|192.0.2.87/24' \
    ip6_addr='mydmz|2001:db8::87' \
    resolver='nameserver 2001:db8::fe;search mydomain.example.com'
  
  sudo iocage start mqtt

Install the MQTT broker::

  sudo iocage pkg mqtt install mosquitto

(rumqttd looks interesting, but mosquitto is packaged. Unfortunately,
as it turns out, the pre-packaged version doesn't include web socket
support.)

Configure the broker - write in
``/usr/local/etc/mosquitto/mosquitto.conf``::

  log_dest syslog
  log_type all
  connection_messages true
  password_file /usr/local/etc/mosquitto/passwd

Most of the defaults are suitable, and the comments in the config file
are ... ok. It appears that the parsing of the file is stateful: the
way you would include websocket support is ::

  # normal MQTT
  listener 1883
  # now websockets
  listener 8080
  protocol websockets

And then would everything afterward configure the websocket listener?
I don't know: the build configuration for the package doesn't include
websocket support, and while it's easy enough to build a custom one, I
can't presently be bothered.

The reason I started wanting websockets was that I found someone who
wrote some JavaScript to subscribe to a data flow over MQTT, and graph
it using DyGraphs, a pretty simple-looking JavaScript graphing
library. If I'd done that, I could have had no more server-side
software. All the state would be in the browser. Very simple, a
minimum viable product perhaps, but no stored history. That's why I
don't mind dropping websockets.

OK, create some MQTT users, for example::

  mosquitto_passwd -c /usr/local/etc/mosquitto/passwd router-username

A bunch of firewall wrangling on both the router and the jail host,
and at length you can see collectd's messages inside the MQTT jail::

  mosquitto_sub -h mqtt -u some-user \
    -P omigosh-passwords-on-the-command-line \
    -t collectd/\# -v

Note that ``#`` appears to be some kind of wildcard in MQTT parlance,
but of course you don't want the shell thinking you are commenting, so
you have to escape it. It seems you can listen to the topic ``#`` to
get every message anyone says; but `you can't list the topics`_. (In
case of bit rot: answers pointed out that you can listen for
everything, that the broker does not keep a persistent list of topics,
and how should it? What if I say something to a topic, and a week goes
by? Does the topic still "exist"?)

.. _`you can't list the topics`: https://stackoverflow.com/questions/42559890/request-all-published-topics

Ahead
-----

This gets CPU usage, system load, signal strength per wireless
interface, process stats globally and for a couple of processes I care
about, etc. and sends them to the MQTT broker.

From here, I need another collectd that will subscribe and get all
these metrics, and save them using collectd's rrdtool plugin; and an
apparatus to make a dashboard out of all the graphs (here I am not
afraid to write some HTML and/or a little script) and to serve them
(darkhttpd, likely). I would like live graphs, but they are not
compulsory.

Also we have no stats per wireless station (STA): all the premade
wireless stuff is kind of assuming you *are* a station, not an access
point. But there is a Lua plugin for collectd, and a way to `talk to
ubus from Lua`_ using ``libubus-lua``, and ``rpcd-mod-iwinfo``
provides a way to get `iwinfo output`_ from Lua. This is much
preferable to running the actual ``iwinfo assoclist`` command and
trying to parse its output.

.. _`talk to ubus from Lua`: https://openwrt.org/docs/techref/ubus#lua_module_for_ubus
.. _`iwinfo output`: https://openwrt.org/docs/guide-developer/ubus/iwinfo

``rrdtool`` is really made for predetermined sets of metrics - but
what isn't? - so there may be some footwork to construct databases for
each station MAC as and when it exists, and make the set of graphs
similarly dynamic.
