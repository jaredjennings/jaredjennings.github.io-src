redundancy file format
######################
:date: 2016-02-06 04:09
:author: jaredj
:category: Backup
:slug: redundancy-file-format
:status: published

First, I'll collect the inspirations for this and the attributes I'd
like to be true of it.

par2 is the biggest inspiration. It shows how to make a file that will
work even if parts of it are corrupted, and which parts are needed. It
makes a lot of sense, but it's somewhat grotty. It uses ASCII, it uses
MD5 in a world where that's getting difficult for security-conscious
users, and it uses 16-bit Reed-Solomon coding, which is slow and hard to
speed up.

Once I read about Blender's DNA, the idea that each file describes
itself, and each version of Blender contains a description of what it
can read out of a Blender file. As a result, you can open a file made in
Blender 1.00, some twenty years later, in Blender 2.76—and vice versa
too. This is a quality I want.

I've also read a lot about RDF; it's very nice to be able to make up a
globally-scoped name for some concept and use it to describe other
things. There's a
`document <https://www.w3.org/2001/tag/doc/selfDescribingDocuments.html>`__
about the self-describing quality of the Web that brings this somewhat
into perspective.

One thing that's been hard to nail down about both RDF and XML is when
you want to digitally sign them: you must first come up with a canonical
set of bits representing the stuff you want to sign. This takes work and
complexity, and that's no good. So it's tempting to think of making
something on top of RDF HDT, or EXI, but at least at the lowest level,
it has to be chunks with checksums.

I came across a Haskell blog entry about the `rule of least
power <https://www.w3.org/2001/tag/doc/leastPower.html>`__. The blog
entry is lost to time, but this W3C page seems to say the sort of things
needed. This may fly in the face of the self-describing DNA sort of
idea: a file format containing its own definition, which must be used to
be certain of reading the file, is certainly quite powerful.

I found liberasurecode, which brings together erasure code, um, code,
from multiple sources under one API. It claims extensibility, but
contains a bunch of case statements and no dlopens. A frightfully static
sort of extensibility, then. And no turbocodes.

Attributes:

longevity
    The format must make sense in ten years, and some tool usable to
    read and write it must exist and be usable in ten years. This might
    mean support for, e.g., multiple digest algorithms. Or it might
    quite explicitly not.
self-description
    The file should say how to read itself, and what it says should be
    true. That is, the self-same specification of the file format that
    gets written in the file should also be used in the construction of
    the tool.
robustness
    If a part of the file is corrupted or unreadable, the rest of the
    file should still be readable.
orthogonality
    If any other tool can do something that might be part of what this
    file could do, the other tool should be used in preference to
    integrating the functionality into this format.
security
    Functionality of a tool that adds redundancy means that when random
    errors are introduced the data can still be recovered. But what if
    the errors aren't random? It shouldn't be possible to crash the tool
    nor change the data.
speed
    It should be much faster than par2.
maintainability
    This, and speed and security, mean using some language like Go,
    Rust, or Haskell. I'd say Java, but that's unmaintainable on the
    runtime side, and may be impermissible to install in ten years...

par2 (and even more par3) have fancy features like encoding a whole
directory full of files of different sizes, or encoding changes to files
(I assume by adding more onto the end of a parity archive with an
existing file already in it). For the purposes of backup, dar already
does these things handily enough in my estimation. Just like gzip just
compresses and does not also archive, I think a redundancy format should
just redound, and not also archive. This could hurt usability for people
who aren't me.

I think the format should have two pieces: the part that
compartmentalizes the file into chunks and the part that produces the
redundancy data. Like video files have container formats and codecs. The
chunk part could be TIFF, HDF5, SDDS, EXI, etc, except that none of
these have magic numbers and checksums built into the idea of their
chunks.

Name ideas (these will turn into magic numbers, file extensions, and
mime types):

-  verily—oh, junk, Google Life Sciences just got renamed to this last
   December
-  KETCHUPCOLLOQUY (thanks /dev/urandom)
