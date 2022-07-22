redundancy files
################
:date: 2016-02-06 01:32
:author: jaredj
:category: Backup
:slug: redundancy-files
:status: published

I've done some reading about various kinds of codes (thanks again,
Wikipedia). I've found that while Reed-Solomon is a good code, it takes
a lot of computation to encode as compared to some others. Most
interestingly, turbocodes seem faster and the patent on them just
expired in 2013. They are used in LTE, and so most of the software that
encodes and decodes them purports to be simulating operations that would
normally be performed by purpose-made chips, rather than just
implementing the turbocode for its own sake. I've found a paper from
2013 that says they tried to make a turbocode decoder for a GPU and it
wasn't as fast as the one for the CPU. That's ok with me, as long as
it's fast: running on a CPU only is simpler and therefore more likely to
still work in ten years.

Using these would mean starting my own file format, rejecting par2. And
the par2 specification is under the GFDL, a sort of dubious and onerous
license. I want to be more self-describing anyway.
