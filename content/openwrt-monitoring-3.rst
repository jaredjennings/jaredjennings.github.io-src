OpenWRT monitoring, part 3
##########################
:date: 2022-11-26 14:17
:author: jaredj
:category: Home IT

I've just realized that my phones probably randomize their MAC
addresses. To try to track the history of their signal quality
individually, I'd have to figure out which device is which using some
other means than the MAC address. If I don't, I'd end up making
thousands of rrdtool files to hold signal quality history for
ephemeral MAC addresses that are never used again after an hour or
two.

The first idea I had was to check the hostname in the DHCP leases
file, ``/var/dhcp.leases``. But only one of the phones told the DHCP
server a hostname, and it was the name of the phone's model. We don't
have two of the same model, so that's not bad, but no other devices
uttered a hostname.

I wanted to track individual device signal qualities in case radios
vary. But even if I were to succeed now, later devices would likely
have improved privacy measures, and I don't want to play
cat-and-mouse.

Failing individual tracking, we could aggregate. If we were to average
all of them, that would not be useful. Perhaps we could take the best
and worst of each metric? Or hash the MAC addresses into *n* bins,
like maybe ten of them? Individual devices would jump between
bins... I'd probably still just want to know what the best, average,
and worst are. Make a change, see if it improves the worst.

Oh - I did want to find out whether roaming is working... I guess that
would have to be calculated in a place where I can see the station
data from all the routers, to see that a station disappeared from one
router and showed up at the other. But if I aggregated the station
data, it wouldn't be possible to determine this... Eh, maybe just send
from the routers the data we can see there, and do fancy things
elsewhere, before storing the data in rrdtool files to graph. Since
I'm sending over MQTT, I could make an MQTT client, not at all related
to collectd, that absorbs the per-station data, does a smart thing,
and outputs both indications of roaming, and a fixed number of pieces
of wisdom, all derived. Then collect and graph.
