OpenWRT monitoring 2: Lua boogaloo!
###################################
:date: 2022-11-26 00:14
:author: jaredj
:category: Home IT

In our exciting previous installment, I lamented the lack of
per-station wireless metrics, but noted iwinfo can get them and Lua
scripts can be written for collectd. So now I've hacked one up.

I learned from the `collectd-lua(5)`_ man page that you use
``collectd.dispatch_values`` to send metrics out of your Lua script to
wherever collectd makes them go; but that man page was a little sparse
on what the exact keys and values in the table should
be. `collectd-perl(5)`_ was a little more verbose about that, but
assumed I knew more about collectd's internals than I did. But hey,
this is Free Software, so I dug into `the source`_ and found the part
that takes up the table I send over.

.. _`collectd-lua(5)`: https://www.systutorials.com/docs/linux/man/5-collectd-lua/
.. _`collectd-perl(5)`: https://www.systutorials.com/docs/linux/man/5-collectd-perl/
.. _`the source`: https://www.systutorials.com/docs/linux/man/5-collectd-perl/

Empirically, I found that the ``host`` and ``time`` values are best
not provided, because they will be properly filled in, and I didn't
see any really good way to get the hostname from Lua anyway.

.. _`types.db(5)`: https://www.systutorials.com/docs/linux/man/5-types.db/

``type`` is the name of a `type`. Many of these are listed in the
`types.db(5)`_ file, and you can define more. I ended up having to do
this. Here's a type that has multiple values::

  if_octets               rx:DERIVE:0:U, tx:DERIVE:0:U

The way to send a metric of this type from Lua is pretty simple::

  collectd.dispatch_values({..., type="if_octets", values={5,3}})

But the type has to be set up for this. In the info about each station
available from this command - ::

  ubus call iwinfo assoclist '{"device": "wlan1"}'

(fill in your own wireless device name) - I found these values::

  "rx": { ...
      "mhz": 20,
      "rate": 6000 },
  "tx": { ...
      "mhz": 20,
      "rate": 72200 ... }

So you can have different bandwidths and bitrates for sending and
receiving; and those may go up or down depending on conditions, so I
want to keep track of them. But the closest built-in type for "rate"
is "bitrate," which only has one value, not separate rx/tx
subvalues. And I didn't find any good built-in type to which
correlating "mhz" would make sense.

So, with reluctance (because the types.db man page points out that you
have to contrive to make your custom types available on every system
where they matter), I began a custom-types.db file with these entries::

  wireless_mhz            rx:GAUGE:0:65535, tx:GAUGE:0:65535
  wireless_rate           rx:GAUGE:0:U, tx:GAUGE:0:U

This, this is why I like collectd better than snmpd. Clearly, if I
didn't control the software on my router, I could not have added
these; and SNMP is aimed at the case where it gets baked into software
you don't control. But if I didn't control the software, I'd have to
get an expensive router to even get SNMP visibility. Anyway SNMP feels
like a straitjacket and collectd doesn't.

I wrote those lines in ``/etc/collectd/custom-types.db`` and added
these lines to ``/etc/collectd.conf``::

  TypesDB "/usr/share/collectd/types.db"
  TypesDB "/etc/collectd/custom-types.db"

With the custom types in place, here's the script I hacked up, because
it's only 100 lines so I'm not making it a git repo::

  require "ubus"

  if collectd then warn = collectd.log_warning else warn = print end
  if collectd then err = collectd.log_error else err = error end
  function errs(messages)
    if collectd then
      for i, m in ipairs(messages) do
        collectd.log_error(m)
      end
    else
      error(table.concat(messages, ". "))
    end
  end
  if collectd then
    values = collectd.dispatch_values
  else
    function values(t, indent)
      if not indent then indent = 0 end
      for k,v in pairs(t) do
        if type(v) == 'table' then
          print(string.rep("\t", indent) .. k .. ":")
          values(v, indent+1)
        else
          print(string.rep("\t", indent) .. k .. "\t" .. v)
        end
      end
      if indent == 0 then print() end
    end
  end

  stats_for = {
    {key="signal", type="signal_power"},
    {key="signal_avg", type="signal_power", instance="avg"},
    {key="noise", type="signal_noise"},
  }
  tx_rx_stats_for = {
    {key="packets", type="if_packets"},
    {key="bytes", type="if_octets"},
    {key="rate", type="wireless_rate"},
    {key="mhz", type="wireless_mhz"},
  }

  function read()
    local conn = ubus.connect()
    if not conn then
      err("Failed to connect to ubusd")
      return 1
    end

    local devices_answer = conn:call("iwinfo", "devices", {})
    if not devices_answer.devices then
        warn("No 'devices' in ubus iwinfo devices return value")
        return 1
    end

    local assoclist_errors = {}
    for i, d in ipairs(devices_answer.devices) do
      local safe_d = string.gsub(d, "-", "--")
      local assoclist_answer = conn:call("iwinfo", "assoclist", {device=d})
      if assoclist_answer.results then
        for j, r in ipairs(assoclist_answer.results) do
          local instance = safe_d .. "-STA-" .. string.gsub(r.mac, ":", "-")
          for k, stat in pairs(stats_for) do
            local av = {
              plugin="iw-assoc",
              plugin_instance=instance,
              type=stat.type,
              values={r[stat.key]}}
            if stat.instance then av.type_instance = stat.instance end
            values(av)
          end
          for k, stat in pairs(tx_rx_stats_for) do
            local av = {
              plugin="iw-assoc",
              plugin_instance=instance,
              type=stat.type,
              values={r.rx[stat.key], r.tx[stat.key]}}
            if stat.instance then av.type_instance = stat.instance end
            values(av)
          end
        end
      else
        table.insert(assoclist_errors, "No result for "..d.." in ubus iwinfo assoclist return value")
      end
    end

    if #assoclist_errors > 0 then
      errs(assoclist_errors)
      return 1
    end

    conn:close()
    return 0
  end

  if collectd then
    collectd.register_read(read)
  else
    read()
  end

To get it to run, I had to add these lines to my ``collectd.conf``::

  LoadPlugin lua

  <Plugin lua>
    BasePath "/etc/collectd/lua"
    Script "ubus-iwinfo.lua"
  </Plugin>

I made it so you can also run it from the command line, outside
collectd::
  
  lua ubus-iwinfo.lua

It asks ubus for the wireless devices, and for each of these it gets
the ``assoclist``, the list of associated stations. Then it dispatches
a number of values for each station, naming them by MAC address.

So that's the collection part done! Now I can see in my
``mosquitto_sub`` output lines like these::

  collectd/myrouter/iw-assoc-wlan1-STA-A0-11-22-33-44-55/signal_power 1669441792.852:-52
  collectd/myrouter/iw-assoc-wlan1-STA-A0-11-22-33-44-55/signal_power-avg 1669441792.853:-52
  collectd/myrouter/iw-assoc-wlan1-STA-A0-11-22-33-44-55/signal_noise 1669441792.853:-95
  collectd/myrouter/iw-assoc-wlan1-STA-A0-11-22-33-44-55/if_packets 1669441792.853:70.9108657070208:82.8958007560948
  collectd/myrouter/iw-assoc-wlan1-STA-A0-11-22-33-44-55/if_octets 1669441792.853:8244.83555196367:122456.062485011
  collectd/myrouter/iw-assoc-wlan1-STA-A0-11-22-33-44-55/wireless_rate 1669441792.853:6000:72200
  collectd/myrouter/iw-assoc-wlan1-STA-A0-11-22-33-44-55/wireless_mhz 1669441792.855:20:20
  collectd/myrouter/iw-assoc-wlan1-STA-08-00-01-02-03-04/signal_power 1669441792.856:-56
  collectd/myrouter/iw-assoc-wlan1-STA-08-00-01-02-03-04/signal_power-avg 1669441792.856:-55
  collectd/myrouter/iw-assoc-wlan1-STA-08-00-01-02-03-04/signal_noise 1669441792.856:-95
  collectd/myrouter/iw-assoc-wlan1-STA-08-00-01-02-03-04/if_packets 1669441792.856:6.1918515443603:6.1918515443603
  collectd/myrouter/iw-assoc-wlan1-STA-08-00-01-02-03-04/if_octets 1669441792.856:2003.55951814726:3259.80391944196
  collectd/myrouter/iw-assoc-wlan1-STA-08-00-01-02-03-04/wireless_rate 1669441792.858:130000:144400
  collectd/myrouter/iw-assoc-wlan1-STA-08-00-01-02-03-04/wireless_mhz 1669441792.858:20:20
  collectd/myrouter/iw-assoc-wlan1-STA-10-AA-BB-CC-11-22/signal_power 1669441792.858:-62
  collectd/myrouter/iw-assoc-wlan1-STA-10-AA-BB-CC-11-22/signal_power-avg 1669441792.858:-61
  collectd/myrouter/iw-assoc-wlan1-STA-10-AA-BB-CC-11-22/signal_noise 1669441792.859:-95
  collectd/myrouter/iw-assoc-wlan1-STA-10-AA-BB-CC-11-22/if_packets 1669441792.860:0:0
  collectd/myrouter/iw-assoc-wlan1-STA-10-AA-BB-CC-11-22/if_octets 1669441792.860:0:0
  collectd/myrouter/iw-assoc-wlan1-STA-10-AA-BB-CC-11-22/wireless_rate 1669441792.861:6000:86700
  collectd/myrouter/iw-assoc-wlan1-STA-10-AA-BB-CC-11-22/wireless_mhz 1669441792.861:20:20
  collectd/myrouter/iw-assoc-wlan1-STA-8E-99-88-77-66-55/signal_power 1669441792.861:-45
  collectd/myrouter/iw-assoc-wlan1-STA-8E-99-88-77-66-55/signal_power-avg 1669441792.862:-45
  collectd/myrouter/iw-assoc-wlan1-STA-8E-99-88-77-66-55/signal_noise 1669441792.862:-95
  collectd/myrouter/iw-assoc-wlan1-STA-8E-99-88-77-66-55/if_packets 1669441792.863:0.0998703777728744:0
  collectd/myrouter/iw-assoc-wlan1-STA-8E-99-88-77-66-55/if_octets 1669441792.863:2.39689666698687:0
  collectd/myrouter/iw-assoc-wlan1-STA-8E-99-88-77-66-55/wireless_rate 1669441792.863:6000:144400
  collectd/myrouter/iw-assoc-wlan1-STA-8E-99-88-77-66-55/wireless_mhz 1669441792.864:20:20

Nice! Now I just have to graph these.
