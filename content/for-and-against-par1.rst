for and against PAR1
####################
:date: 2016-02-07 01:56
:author: jaredj
:category: Projects
:slug: for-and-against-par1
:status: published

PAR2 is better than PAR1. Why? Because it can deal with different-sized
input files, it can store different numbers of parity blocks in parity
files, and it can read parts of corrupt parity files.

But how does darbrrb use PAR2? Upon dar slice files that are all one
size. darbrrb directs PAR2 to store an identical number of parity blocks
in each parity file, so they will be of predictable and identical size.
And darbrrb requests a quite conservative amount of parity, and uses
small slices and parity files, on the theory that if an optical disc
fails to produce some bytes in the middle of a file, it will fail to
produce the rest of the file as well, but might (untested) successfully
produce the next file. In other words, there's a reason PAR2 is
overcomplicated for darbrrb's uses: darbrrb only needs PAR1.

And Gibraltar calculates 8-bit Reed-Solomon codes really fast, and
par2cmdline still recovers from PAR1 files. So there's fast encoding,
and a strong fallback.

But PAR1 depends on a technical specification of Reed-Solomon
calculation that's broken. So Gibraltar will likely not produce the same
bits as the PAR1 spec says, the bits par2cmdline could decode.

So I think a new format is still needed. But PAR1 might make a better
base for it than PAR2, and the PAR1 spec is public-domain. That's easier
than the GNU FDL.
