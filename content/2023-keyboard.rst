Modelling an ergonomic keyboard in 2023
#######################################
:date: 2023-01-13 23:35
:author: jaredj
:category: Keyboards

The tshort Dactyl Manuform I made as a temporary fix until I finished
my own keyboard design has been working great for about three and a
half years now.

What of my own design? I have not taken it up lately, what with 8-bit
computing, TheHive/Cortex, and other things. Previously I looked hard
at libfive, a functional representation (f-rep) CAD kernel, but
couldn't get into a flow with it. I looked at the ErgoWarp, which is
written in OpenSCAD, but it blew up when I tweaked it too much, and to
find that it purported to be based on a good model of the hand, but
still had (and therefore needed) tweaks in the original code, was
demoralizing. I looked at the Dometyl, written in OCaml, but it didn't
seem succinct or beautiful, and the OCaml toolchain was big in a time
when I had started looking for smaller languages.

Lately I've been swayed by joshreve's comments about using CADQuery
instead of OpenSCAD. If I'm going to use a big ball of code I didn't
write, it ought to put out a `non-pathological`_ model. And I want to
make a keyboard using curves, and while you can express Bézier curves
and patches in OpenSCAD, you are kind of using it as a giant
calculator at that point. I looked at
https://github.com/joshreve/dactyl-keyboard. I could see translations
of a lot of the same constructs found in the Dactyl Manuform, and they
didn't seem as nice in Python.

.. _`non-pathological`: https://github.com/tshort/dactyl-keyboard/issues/22

So what else can use OpenCASCADE? `awolven`_ bound version 7.1.0 to
Common Lisp a year or two ago. But that OpenCASCADE version is
from 2016. Given that it's a lot of C++, and the binding includes a
custom version of SWIG and some manual patching instructions, I can't
imagine it would be easy to update this binding. There's a Java binding
for OpenCASCADE, which could be used by Clojure... oh, it's commercial
software. I've always wanted to avoid licensing fees as an entry cost
for new users of this sort of code.

.. _`awolven`: https://github.com/awolven/oc

Having already read all this on the topic tonight, I figured to write
down what I'd found; but now I remember that another thing I decided,
last time I was thinking about this project, was that I had not
printed enough different keyboards designed by other people.
