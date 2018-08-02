silly homelab gyrations
#######################
:date: 2018-08-01 22:58
:author: jaredj
:category: Projects

OK so let me tell you about this silly thing. Well first I'm still
making a keyboard but I'm on a week-or-two break because our car is at
the mechanic. There are things to say about that but during the break
I'm working on some home IT tasks.

So I decided to set up Nextcloud because ① it can slurp photos off my
phone, ② it can sort of manage them, and ③ it has a community of
people who write integrations between it and other software. So I set
up Nextcloud 11 in a FreeBSD jail. Cool times, right? It was just for
evaluation, against a couple other pieces of software. But it stuck
and now I have 9GB of stuff in it. I never did anything that would be
necessary to let it face the Internet, I never set up HTTPS, and
between then and now I've heard a thing or two on `BSD Now`_ about
databases on ZFS.

.. _BSD Now: http://bsdnow.tv/

So it has to be said that's a good deal of technical debt. I have to
upgrade it because my phone keeps updating the app, and it seems the
app won't talk to the website anymore. Obstacle 1: we're on Nextcloud
13 now. So I had to upgrade to Nextcloud 12 first, then
to 13. Obstacle 0: my IPv6 deployment is in shambles and it makes
FreeBSD unable to get its packages. Fixed that. OK Obstacle 2: they
changed how Nextcloud is packaged for 13, and have support for three
versions of PHP 7.x. Oh right, maybe I should upgrade PHP. Well, I
should make the ZFS datasets right. Eh, I should have the MySQL
running outside the jail with the web server in it. While I'm at it, I
should follow all the directions in `John Ramsden's howto`_. Ah but he
brought his data in with NFS, and my whole DMZ FreeBSD box is not on
mirrored disks, and my photos really should be. OK so I'll - well, to
open up this Nextcloud server to the Internet, I'm going to at least
want it to send logs somewhere. I need a log server, I never set one
of those up. So my little Debian Stable VM that's serving NFSv4 with
Kerberos security, I was going to set it up to save logs. Well - the
mirror on that box wasn't ever really that great, it's just what my
old QNAP NAS could handle, it would be better to store all that stuff
with ZFS, right? And I was going to set up a FreeBSD box to serve
that, separate from the DMZ box. Should my logs land in a database?
Slow writes, not sure how often I'm reading them, nah. Oh, I did tell
that Splunk guy I would look at Splunk Free... [reads EULA] no thanks,
not at this time would I like to run more software I can't pry inside.
But hey maybe I should set up FreeNAS. It'll be easier to manage. Oh
look there's a Nextcloud plugin. Um kay so now I'm allowing the
Internet to connect to my NAS again? I got away from that a while
ago. Oops, no, it requires 8GB of RAM, and I've only got 24GB for all
the VMs. OK so I set up a straight FreeBSD box, on some free space
I've got on two drives; I sync all my 400GB of files over to it, then
get rid of the LVM volume group mirroring those two big drives, set it
up for ZFS, and shlurp the files there; then I set up a jail on there
for syslogs, and maybe a jail for a database, and just my web server
and Nextcloud PHP code runs on the DMZ box, and it gets files and the
database from the new box.

For those following along at home, this has ballooned from updating a
single package to deploying a completely new VM, moving 409GB of data,
and setting up three new jails. Well—let's get to it, I suppose.

.. _John Ramsden's howto:
   https://ramsdenj.com/2017/06/05/nextcloud-in-a-jail-on-freebsd.html#security
