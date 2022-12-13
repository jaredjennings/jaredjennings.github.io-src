Chickenostracon
###############
:date: 2022-03-09 09:24
:author: jaredj
:category: Backup
:tags: darbrrb, cyanostracon, scheme, chicken, python, curio, dsbmd, udisks2

I wrote a script once called darbrrb, which helps you make backups
onto optical discs with redundancy. That script assumes you have one
optical drive of interest, and it waits for complete burns or reads of
discs to happen on that drive before going on to other things. If you
have multiple drives, so that you could be burning multiple discs at
once, darbrrb cannot put them to proper use.

cyanostracon was the answer to that. It finds out about all the
optical drives you have and burns to them in parallel. Tests indicated
it might work for backup; restore capability was still being built.

But another important capability of darbrrb was to make sure the
backup could actually be restored. The way this happened with darbrrb
was that it would write a copy of itself, a README file, and an
indication of the command line with which it was run, onto every disc;
and it was a single Python 3 script with no dependencies. So you would
need Python 3 and dar installed in order to use it; but the README
said that.

cyanostracon was built around Curio (for asynchronous goodness) and
DBus (the udisks2 protocol provided notification of which drives
existed and when discs were inserted). No problem, we were going to
use pex to package up all those dependencies and make a single file
that could be run with just Python 3. Probably. Somehow.

A big hole in this idea is that the best UI to use while a backup is
running is no longer the command line. Burning a Blu-Ray disc takes a
good 45 minutes - longer than a screen lock timeout - and maybe the
person changing the discs isn't even the same person who started the
backup. The user interface might now be a web or mobile app, or some
kind of home automation thingy. Or maybe the disc switcher could even
be a robot! These are just the use cases I can imagine for
myself. That means the UIs of cyanostracon are not likely to fit in a
single process on the same computer where the backup was begun.

Meanwhile, dsbmd comes into the picture. The machine with the optical
drives now runs FreeBSD and doesn't have a graphics card, so I don't
have the desktop use case that udisks2 was made for, and dsbmd is a
much smaller piece of software that can perform the same purpose. So
small that the way to interface with it might use less lines of code
than interfacing with the rest of cyanostracon in the accustomed way.

When combined with the dynamic that I now have a file server with
several places to back up from, not just my home directory, and that
the simplicity of running my own backups once in a while has not led
to any consistency, the whole thing makes me feel more like
cyanostracon's proper place is not as a single piece of software
running in a single place and doing everything that dar and par don't
do for it.

In fact, it made me take another look at cloud archival services. But
it appears that offering an easily understandable pricing structure is
itself a feature that comes with a price.

So what to do? Why, rewrite cyanostracon in Scheme, of course!

I obtained `Chicken <http://call-cc.org>`_, a Scheme interpreter and
compiler, which can build statically linked single-file executables,
appears to be reasonably small, and has some useful extensions. A
couple of points on hooking it up to Emacs: you need a recent version
of geiser, you need geiser-chicken, and you need the ``apropos`` and
``srfi-18`` eggs installed. I didn't get any decent errors letting me
know that these were the problem, when I tried to evaluate Chicken
code using Geiser and it didn't work. It just didn't work.

Now, Scheme has a wily little procedure
`call-with-current-continuation`. Anyone who has written a page on the
topic (`The Scheme wiki`_ for example) will tell you that you can use
it to build exception handling and coroutines. But it was only on
`this page at the Rensselaer Polytechnic Institute`_ where it was
elucidated that continuations are *what Scheme has instead of a call
stack*. Maybe the effect of reading on the topic was cumulative and
that last page was just when I happened to become slightly more
enlightened, but I managed to build a coroutine scheduler not entirely
unlike Curio.

.. _`The Scheme wiki`: http://community.schemewiki.org/?call-with-current-continuation
.. _`this page at the Rensselaer Polytechnic Institute`: https://www.cs.rpi.edu/academics/courses/fall00/ai/scheme/reference/schintro-v14/schintro_141.html

The great thing about Curio is that it lets you write lots of
concurrent, asynchronous code in a readable way. The easiest way to
implement such code is with `futures` or `promises` or `callbacks`, by
writing functions that begin something, and when it is over call a
function passed in, like::

    def doSomething():
        sleep(5, andThen=doSomethingElse)

    def doSomethingElse():
        ...

But this is nearly the worst way to have the code structured for
understandability and debuggability. In Python, and to a slightly
lesser degree in Scheme, the juxtaposition of two things, ``a b``,
implies a timeor causality relationship between them: ``a`` is
evaluated first, then ``b``. Callback-based programming makes
juxtaposition meaningless. What just happened before the first line of
``doSomethingElse``? What if some code is written after the ``sleep``
call? Will it happen at all? When? Does doSomethingElse happen in the
same thread or does it spawn its own? What if doSomethingElse
encounters an error?

Accomplished users of continuation-passing style (CPS) will no doubt
scoff at my weak powers of understanding, but they can go write their
own backup program if they wish.

Curio lets you just write::

    async def doSomething():
        await sleep(5)
        ...

There's a useful split there, too, that's reminiscent of the system
call interface between a kernel and a userspace application; both
David Beazley (Curio author) and Nathaniel J. Smith (Trio creator)
have things to say about that.

I want that order-preserving, non-parallel concurrency available to me
in Scheme. And I've just managed to build a first attempt at it. This
is probably the answer to an exercise labelled "Easy" in some chapter
of `Structure and Interpretation of Computer Programs` that I haven't
read yet; but I feel accomplished. I'm still trying to figure out how
to make it easy to expand it, and hook it up to asynchronous I/O, and
make it available as an egg, test it, test things made with it, and
finally get back to my quixotic reimplementation of cyanostracon.

EDIT
====

Uhhh. So the farther I got implementing that, the more I learned that
*this is how Chicken already does threads natively*. I should have
read up on it more. I still feel good about grokking call/cc.
