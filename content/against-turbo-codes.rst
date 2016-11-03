against turbo codes
###################
:date: 2016-02-06 15:12
:author: jaredj
:category: Projects
:slug: against-turbo-codes
:status: published

Upon reading a few more papers, I find that the reason people only
simulate turbo codes in software is because decoding them is so
computationally difficult that for the applications they are used in
(phones and TVs) people make custom silicon or write programs for DSPs
in order to decode them. Furthermore, the use of SIMD instructions (e.g.
MMX, SSE, etc) in Reed-Solomon codes has been asserted to be patented
(start from `the par2cmdline
issue <https://github.com/Parchive/par2cmdline/issues/33>`__ about it)
and taken down. No one is at this point trying to say RS codes are
patented, I think: they are old. But if they can still be obstructed by
patents, so much more can Turbo codes.

Furthermore, making a new file format is not predicated on using turbo
codes: the reason to make a new format is to gain the advantages of par2
over par1 without being locked to 16-bit RS codes. 8-bit RS codes are
serviceable; Gibraltar provides fast encoding and decoding of these,
now; and there are many other efforts regarding 8-bit RS codes, some in
OpenCL I think, which is not locked to a GPU, much less any particular
GPU.

So, for a new file format, it's advantageous to figure out how to use
8-bit RS first.
