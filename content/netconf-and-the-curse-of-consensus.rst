NETCONF and the curse of consensus
##################################
:date: 2016-05-01 02:07
:author: jaredj
:category: Uncategorized
:slug: netconf-and-the-curse-of-consensus
:status: published

So my router runs OpenWRT, and its configuration is complicated enough
that I can't easily capture it all in one place, nor set up a new blank
router to do its job if need be. There are packages to install, UCI
settings to set, configuration files to put in place, and maybe a change
or two to an /etc/init.d script. And the firewall config when written in
UCI gets repetitive really fast.

I wanted Puppet, but that's too big by far, especially now that Puppet
has copies of all its own dependencies (i.e., its own Ruby interpreter
and set of gems) inside the official packages. And someone's done it
before and it's petered out.

I always sort of thought Puppet was too big: cfengine 2 did 50% of what
Puppet did, while being much smaller. I'd never trade back now, because
cfengine 2 wasn't extensible to new resource types, its syntax was not
good, and cfengine 3 syntax is downright bad.

I've wanted for a long time to be able to link compliance with config
policy (see back through the "Compliance at home" category), and the
cool kids (Salt, Ansible) are using YAML these days, so why not use RDF,
encoded in something light like Turtle? It's the ultimate in
linkability. And RDF HDT for wire transfers, or something. But I thought
through what I would need to write a decent system configuration, and
something like Puppet's classes and facts would be necessary. Well - one
of the biggest things OWL does is to classify resources based on
information, i.e. to figure out what classes things have based on facts
about the class and the thing. But no one seems to have tried to make a
small-footprint OWL inference engine. And I found that the Rete
algorithm, which makes inference fast enough to be possible, does so by
trading memory use for CPU work. That may not scale on a router. (On
second thought, I haven't figured out what the scale might need to be.)
So RDF might be too heavy for a router to deal with.

OpenWRT has Lua, though: perhaps I could just write a set of functions
in Lua, calls to which constitute the desired state of the system; the
functions would check the state and change if necessary. This is the way
of Lua: munge code in with data. Power in a small size, at the possible
expense of easy security. Make a package with the desired-state function
definitions; rsync the description of the desired state up; no packaging
RDF libraries, no C work (Rust would be nicer but I can't quite get it
to cross-compile yet, there's some little mips h file missing): quicker,
smaller, nicer. So I'm reading through the Lua reference manual again.

Meanwhile I find out about NETCONF, which is XML-based network device
configuration getting-and-setting, with flexible transports underneath,
but most likely presented as an SSHv2 subsystem. It probably will only
do UCI settings, not also put arbitrary config files in place (e.g.
ntpd.conf, gpsd.conf, sshd\_config), but it's already standardized and a
server is already packaged for OpenWRT.

So now to my main complaint: worse is better. NETCONF is made of XML not
ASN.1 BER, woohoo I guess. But it's still grotty, and I think it's
because no one could agree on anything cooler.

I'd like for the way of configuration to be either made of RDF, or
exposed via a 9P filesystem, or both (that's funny because the Plan 9
folks swear by short strings and local filesystems, and the RDF folks
reckon the URI as the supreme abstraction: long but global). But I don't
think I've got time to both flout the consensuses and do cool things in
the next layer up.
