Clojure code organization
#########################
:date: 2019-06-26 00:24
:author: jaredj
:category: Projects

I started the Dactyl Marshmallow from the Dactyl, written by Matt
Adereth. He wrote all his code in a single file, dactyl.clj. This file
contained definitions for important variables (e.g. how much tenting,
how many rows and columns of keys), shapes (the frame for a single
key, the frame for all the keys pressed by the thumb), and code to
emit OpenSCAD files containing those shapes.

I split the code into multiple files, roughly by shape (e.g. bottom,
sides). I started to centralize important variable definitions in
layout.clj, and added a rudimentary means by which multiple keyboards
could be defined and chosen from. As I wrote more code to describe
shapes, with odds of about 60% I put the important configuration for
that code in the layouts map in layout.clj.

Now I need not only variables, but shape definitions (really the
thumb) to vary between different keyboards. If this were Python, I'd
break out the classes and inheritance at this point, because it is an
obvious way to share most code, but specialize some. But this isn't
Python, and it never was highly designed Clojure either.

It appears I could use multimethods and ``derive`` for this task. Or I
could just throw a function into the layouts map. Or some protocol
inheritance thingy. But I can't think of splitting the code better
without trying to think of how to get the data used by a piece of code
closer to the code.

Some data is just things that could be calculated but were easier to
write down. For example, given a 4 row by 6 column finger part,
without two keys in the corner, it is possible to figure out the key
coordinates of every place around the edge. It was a challenge, and I
stepped around it. Now to keep doing it that way complicates the
definition of each keyboard, where it could be calculated with one
piece of code for all keyboards.

Some data is peculiar to the code that uses it, but when it's all
written together it looks tantalizingly close to a very high-level
description of a keyboard, a description I want to be able to write -
including the part where I can say, "the sides of this keyboard are
the same as everything else, but the thumb part is a little
different."
