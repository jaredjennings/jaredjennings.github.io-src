Backup revelations
##################
:date: 2015-08-30 01:06
:author: jaredj
:category: Backup
:slug: backup-revelations
:status: published

While reading the code of par2cmdline (a month ago or something), I
think I apprehended that the number of input files and the number of
slices for the Reed-Solomon calculations are linked quite closely, and
that perhaps this was why the PAR2 file format moved to using 16-bit
Galois fields instead of the 8-bit fields used by PAR1, because then you
can fit more than 256 files in a PAR2 file. I'm still a bit shaky on
this, but it seems you ought to be able to use 8-bit Galois fields for
as many files as you like - the Gibraltar project was using it for whole
disks, of course.

EDITED TO ADD: Ah, the limit is on the number of output files. Totally
understandable. I'm not ever going to need more than hundreds of output
files for my use case, but I guess someone on Usenet did once.
