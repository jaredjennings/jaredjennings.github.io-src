Push generators and monads
##########################
:date: 2015-06-01 03:19
:author: jaredj
:category: Projects
:slug: push-generators-and-monads
:status: published

I wrote `Shaney <https://github.com/jaredjennings/shaney/>`__
(`history <https://github.com/jaredjennings/shaney/blob/master/requirements.txt>`__)
to parse important elements out of hundreds of text files (Puppet source
code and LaTeX), and produce interesting content out of them, writing it
into dozens of other text files (LaTeX). Now I'm trying to do much the
same thing for
`snailcrusader <https://gitlab.com/sagemincer/snailcrusader>`__, but not
reading only Puppet source files, and not creating LaTeX as output.
Shaney started out as a set of classes whose instances would call each
other's methods, and turned into a set of push generators, thanks to
some `Beazley reading <http://www.dabeaz.com/coroutines/>`__, becoming
several times faster in the process. It's small code and fast, but not
easy to read and write, so I wanted to make the syntax a little nicer.
But in attempting to do so, I've been bothered by the similarities
between push generators and monads.

So I went back to my favorite document on monads, `You Could Have
Invented
Monads <http://blog.sigfpe.com/2006/08/you-could-have-invented-monads-and.html>`__
from Dan Piponi. There are many monad implementations for Python, but I
doubt they are fast enough, because they are using functions and not
generators. YCHIM doesn't start from what exists in Haskell, but from
the problems that could have incited you to invent monads. So it makes
it easier to see sort of which half I've implemented. Now let's see if
all that untangling and concept-naming can help me generalize and
sweeten what I've got, enhance shaney, and create snailcrusader. You can
follow the effort at https://gitlab.com/jaredjennings/python-textpush.
