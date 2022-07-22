Why I'm not running Qubes OS
############################
:date: 2016-01-13 03:42
:author: jaredj
:category: Security
:slug: why-im-not-running-qubes-os
:status: published

`Qubes OS <https://www.qubes-os.org/>`__ uses virtualization to greatly
enhance system security, for example by running the code for the network
stack and the code for the firewall in separate virtual machines.

But:

-  NVIDIA proprietary drivers aren't supported, but I'm trying to use
   libgibraltar, which needs CUDA, which needs the proprietary drivers.
-  Qubes has no IPv6 support, but I'm trying to use IPv6 only where
   possible on my home network, or at least dual-stack.
-  They're aiming primarily at Intel processors, but I use AMD. (weak
   reason)
-  There was some other reason, but I forgot it.
