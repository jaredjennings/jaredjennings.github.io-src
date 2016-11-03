System configuration management woes
####################################
:date: 2015-09-19 02:34
:author: jaredj
:category: Uncategorized
:slug: system-configuration-management-woes
:status: published

First, there aren't enough prebuilt packages for system configuration
management software (e.g. Puppet, Chef, Ansible, Salt) for ARM.

Then about Puppet's modules. They are supposed to be a great help: I
want to configure a subsystem, I go to the Puppet Forge and find a
module, I use the module. But it seems all the most popular modules
merely manage to squish all the configuration of the subsystem into
class parameters, turning my Hiera config files into just everything
config files. There are relatively less successful modules that are more
opinionated, but there's no way to tell whether their opinions about how
the subsystem should be configured will be helpful to me: no one steps
back from their work and compares it to the work of others, and I've
seen no historical information of the form, "I started with x module by
author y. It didn't z and I needed it to, so I made some changes."

I thought I was going to inject security compliance into the mix. But
that was itself short-sighted: where I was, we couldn't have something
if we couldn't secure it, so I reckoned module authors would welcome
changes that would improve security, and possibly worry about comment
bloat as I added in a bunch of metadata. But in the outside world,
security is one of the things that makes stuff not work. I always knew
you couldn't just flip a switch - CMITS has many interdependencies that
have been challenging to tease out - but I never reckoned that even if
such a switch existed, there are people who don't even want to walk
close to it.

Finally, everything decent is too big, and everything small enough is
substandard. This means: Puppet (pre-4; they didn't build 4 for ARM)
requires 23 packages. Salt may have been smaller (they didn't build for
ARM) but come on: executable YAML? (This is a Puppet talking point, but
that doesn't make it false.) I want something written in Rust that
consumes Lua or Scheme or something small like that. Then maybe I could
run it on my routers too.
