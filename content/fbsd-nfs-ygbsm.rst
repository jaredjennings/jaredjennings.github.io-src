FreeBSD NFS YGBSM
#################
:date: 2018-09-18 00:19
:author: jaredj
:category: Home IT

Seriously?

So I fell back to NFSv4 sec=sys, which proceeded to fail with a storm
of packets that did not abate when I terminated the hanging mount
command on the Linux box. The Linux box would try to start a client
session, and the FreeBSD box would tell it that its handle was stale.

Fine! As long as we're doing sec=sys, let's do NFSv3! That's what all
the howtos are about anyway. So I got that all set up, but the nfsd
refused to register itself as an RPC service, and both Linux and
FreeBSD clients said program 100003 was missing. (That is the assigned
program number for nfs, as I found.)

You guys. YOU GUYS.

Back a month or two ago, in my haughtiness, I set the sysctl
vfs.nfsd.server_min_nfsvers to 4. But I didn't notice
vfs.nfsd.server_max_nfsvers, which was still 3. There was no NFS
version that server could serve! *facepalm*

First, when I set server_min_nfsvers to 3 and restarted nfsd, behold,
it registered itself as an RPC service! And then when I set
server_max_nfsvers to 4 and did an NFSv4 sec=sys mount, it worked! And
then when I set sec=krb5i it worked! From the Linux box, anyway. The
FreeBSD client mount is exiting immediately; ``mount`` says there's an
NFS filesystem mounted on my mountpoint; but no files show up. Still
working on that one.
