ISO9660 vs. UDF, for backup storage
###################################
:date: 2022-11-03 23:00
:author: jaredj
:category: Backup

I've been working on cyanostracon again. Ever since darbrrb, my
strategy was to write ISO9660 filesystems to Blu-Ray media. UDF seemed
too glitzy and new. But I never made sure about that.

After a dive into the FreeBSD handbook and man pages, and Wikipedia, I
find that for my purposes, UDF is indeed unnecessary, and I can ignore
it. It seems most of its enhancements are around supporting
rewritability better, and I'm not interested in rewriting my
backups. Blu-Ray players might not play my discs - but I'm not trying
to make video discs. OS platform support is not as wide as
ISO 9660. And it seems the way to mount a UDF disc in FreeBSD is to
use ``mount_udf(8)``, since FreeBSD 5.0. If they couldn't manage to
fit it into the usual ``mount(8)`` utility, I don't want it.
