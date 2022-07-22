FreeBSD NFSv4 woes
##################
:date: 2018-09-16 23:22
:author: jaredj
:category: Home IT
:tags: freebsd, zfs, nfs

I set up a FreeBSD VM to serve my files over NFS from a ZFS
filesystem, having lost some data from an XFS filesystem. My clients
are Debian GNU/Linux and FreeBSD. I have a Kerberos domain and an LDAP
server, so I can have the same usernames and uids across multiple
machines. NFSv4 is the latest version, and has uncomplicated support
for Kerberos. Right?

So my existing Linux VM, with the XFS filesystem (on an LVM mirror,
for all the good it did), serves NFSv4 with sec=krb5p just fine to my
other Linux machines. I could stick ZFS on it, but I've read lately
about a feature flag that ZFS-on-Linux has that no other ZFS has, so
the effect is that you can't take your ZFS pool and import it on
another OS. (This is doubtless a blithe dismissal of a complicated
issue without good cause. Whatever, I wanted to use FreeBSD.)

I found out how to serve NFSv4 from FreeBSD, from the Handbook
(q.v.). I found out what happens when you set the "sharenfs" property
on a ZFS filesystem. I found out that the right things don't happen
when your sharenfs value contains a comma. I've forgotten why by now,
but this means you can't export to multiple subnets using only the
sharenfs property.

So I tell FreeBSD I want to export my filesystem with sec=krb5p, and I
tell my Linux client to mount the filesystem with
sec=krb5p. "Operation not permitted." What? So I use mount -vvv on
Linux (where is this on FreeBSD?), and tail logs on FreeBSD. Not much
to go on (forgot details). End up watching the NFS traffic in
Wireshark. NFS4ERR_WRONGSEC.

So then I began to find the wonders of dtrace in FreeBSD. Where did
that value come from? It seems like when you tell Linux to use a
certain flavor of RPC security, it sort of works up to that. There are
a couple of failures at first. Then it gets right. (I have not found
the wonders of SystemTap in Linux.) It's all a bit murky because I can
only see things at the beginning and end of certain functions in the
FreeBSD kernel. Some important functions are static, i.e. internal,
like ``nfsrvd_compound``; they don't get trace points. Some functions
are not getting called that should be, given what's said over the wire
and what the code of the kernel is. (I've tried this on FreeBSD 11.2
and 12.0-CURRENT, which by now is a month or two out of date.)

I've wanted to ask people who know, but I can't remember what I've
done and not done, and there are so many moving parts that are only
supposed to be necessary for NFSv3, but seem to be at least half
necessary for NFSv4. One case is that to reread the exports file, you
restart mountd, which NFSv4 isn't supposed to use at all. The Handbook
only documents the server side of NFS - it isn't made for the level of
detail I've arrived at, anyway - blogs document NFSv3...

It needs documentation, but from what I can see, it's possible that
Linux should act differently when it is an NFSv4 client, or maybe
FreeBSD should be more forgiving as a server... I've read relevant
parts of the FreeBSD code, but not much of the standard, and none of
the Linux kernel. I feel unwilling to go all the way to the bottom of
this, and write the documentation I wish I'd been able to read.

So I decided to write about it, so I could think. And, hidden in the
second sentence I typed, I find an answer: I have the same uids across
my network. I can use sec=sys. I would like to authenticate my hosts
and users well, rather than trusting hosts, but it isn't worth holding
everything else up. All the hosts are in the same room, and half of
them are on the same physical computer. Maybe someday NFSv4 +
Kerberos + FreeBSD + Linux clients will work for me, but it doesn't
have to be today.
