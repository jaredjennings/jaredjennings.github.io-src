Compliance at home
##################
:date: 2014-01-22 05:41
:author: jaredj
:category: Compliance at home, Projects, Security
:tags: disa, nist, security, srg, standards, stig
:slug: compliance-at-home
:status: published

I'm much more cognizant of the need for secure configuration of
operating system software everywhere than I've ever been in my life—and
at no time in my life have I had less time to worry about securing my
home computers.

The U.S. DoD and NIST have done some solid work in setting out, at
multiple levels of abstraction, how software should be configured for
security. It looks like the top levels of this are set out by the `NIST
Cybersecurity Framework <http://nist.gov/cyberframework/index.cfm>`__
these days; the highest-level standard I'm used to is `SP
800-53 <https://nvd.nist.gov/static/feeds/xml/sp80053/rev4/800-53-controls.xml>`__,
written nicely in some form of XML in this link. The
`DISA <http://disa.mil/>`__ produces
`SRGs <http://iase.disa.mil/srgs/>`__ which speak on how the SP 800-53
requirements apply to categories of products, and
`STIGs <http://iase.disa.mil/stigs/>`__ which say how to apply the
requirements in SRGs to specific products.

As examples of the levels we're talking about, SP 800-53 might have a
requirement that when I, a user of a system, delete some data in the
system, you, another user of that system, should not be able to find and
read that deleted data. Then the UNIX Operating System SRG may say that
an operating system should have a secure, robust multi-user filesystem.
And suppose ElfinSlipper Professional Linux™ provides the capability to
install on a FAT or ext4 filesystem, where FAT can't separate access by
different users and lets anyone access data outside known files, and
ext4 supports multiple users and prevents users from reading anything
they don't own, including the raw disk. Then the STIG for ElfinSlipper
would say that you have to choose the ext4 filesystem when you are
installing ElfinSlipper.

Now, NIST and DISA were promulgating these standards for years before I
took any notice. And if I weren't being paid to read and understand
them, I wouldn't have bothered. I don't have any time to implement them
at home, but I feel insecure not having done so.

More later about what's being done to put security in easy reach of
beleaguered sysadmins, and what should be done instead.
