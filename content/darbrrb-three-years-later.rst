darbrrb, three years later
##########################
:date: 2016-02-02 04:32
:author: jaredj
:category: Uncategorized
:slug: darbrrb-three-years-later
:status: published

In 2013, I wrote `darbrrb <https://github.com/jaredjennings/darbrrb>`__
to make redundant backups onto optical media using dar and par2. After
some testing I found par2 was so slow that backing up my files (a couple
of hundred gigabytes) would take more than a week, not counting the time
it takes to burn each disc.

Somehow or another, around that time I found out about Gibraltar, a
library that computes error-correcting codes using CUDA on an Nvidia
GPU. But not the same kind of code as specified in the `PAR2
spec <http://parchive.sourceforge.net/docs/specifications/parity-volume-spec/article-spec.html>`__:
PAR2 uses GF(2\ :sup:`16`), Gibraltar uses GF(2\ :sup:`8`). I tried to
extend Gibraltar, but the logarithm table necessary for a
GF(2\ :sup:`16`) code is many times larger and wouldn't fit in the
buffers used on the GPU.

I could use PAR1, and maybe accelerate it with Gibraltar. But PAR1 is
old and grotty. It has size limits, ASCII-only filenames, and if part of
a PAR1 file is corrupted the whole file is unusable. PAR2 has larger
limits, and has packets, whereby good parts of a bad file are usable.

Or I could strike out and make my own new redundancy file format, but
the chances are that wouldn't be apt-gettable in ten years, like
par2cmdline already has been.

In the last three years I've gotten a new and faster computer. I
wondered if it might be so much faster as to make backup times more
palatable. It's not, but in the midst of the testing I notice that the
par files are made in serial, and par2 only uses one core out of my
(now) eight. A speedup, for my use case, might be gathered by taking up
the paperwork necessary to run multiple par2 invocations at once, more
easily than by making a 16-bit Reed-Solomon encoder on a GPU when I
don't know CUDA, and much more easily than by making and testing a new
file format and tools.

I tried phpar2, which purports to be multithreaded and five times
faster, but it has too many Microsoftisms: it needs at least an evening
of porting now, not to say what it will need in ten years.

I searched for OpenCL Reed-Solomon engines, and found more than I
expected. Jury's out.
