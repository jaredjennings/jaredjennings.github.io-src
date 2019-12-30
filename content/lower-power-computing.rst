lower power computing
#####################
:date: 2019-12-29 20:26
:author: jaredj
:category: Untangling

Cool introduction later, maybe.

I've been reading about `CollapseOS <https://collapseos.org>`_. It's
an operating system kit for Z80-based computers, built against the
possibility that the supply chain that enables the building of ever
fancier electronics will collapse, the electronics will eventually
cease to work, and people some 100 years from now will need
general-purpose computers with which to program the microcontrollers
still ticking along in so many devices they find around them. In such
a world they will find old devices with Z80 processors in them and
cobble up microcomputers from them, and those computers will run
CollapseOS.

As such its goals are to be easily understandable by people from top
to bottom, malleable to fit such unforeseen computers, capable of
building itself from source to binary after those modifications are
made, and capable of assembling code for microcontrollers and sending
the code to them.

I'm impressed that the author, hsoft, is thinking past his own
lifespan, in a Long Now sort of way; that he has weighed the costs,
risks and benefits of making this thing; that he looked around before
beginning construction to make sure something suitable had not already
been made; and that the project has an impressive set of non-goals
which have focused efforts and enabled thinking the idea that
CollapseOS could be finished. After he began and announced the
project, some people brought up to him things he had not heard of
before; none have entirely effaced the worth of this particular
effort.

Now, I have no love for the Z80. I grew up with Commodore computers,
which had 6502s and their successors in them. The 6502 is even simpler
than the Z80 - 3500 transistors not 9000.

I read a lot about how Forth is made, and how microcomputers are
constructed. I watched videos about AcheronVM and the Cactus
computer. I thought about advancements since the time of those
processors and what it might mean to step down to one.

 * Unicode could be computationally prohibitive: internally it may be
   represented as 32-bit integers; externally, UTF-8 is a
   variable-length encoding. Either way, the space and computational
   power taken to process each single character is multiplied,
   relative to fixed 8-bit characters.
 * A single picture could easily exceed 64K. Transferring it from one
   place to another inside a computer may take seconds, much less
   processing it in any way.
 * Forget about videos.
 * JSON wastes too much space.
 * Python is too big and slow.
 * Any modern multi-user, multitasking OS is of course too big.
 * Even a C compiler is large on an 8-bit machine, and its output is
   flabby compared to hand-written assembly.
 * Shared libraries mostly would not fit.
 * Anything that takes a lot of calculation won't fly without
   tricks. 3D graphics, music.
 * Asymmetric cryptography would take forever.

There are ways to do some of these, but they cannot be the usual
ways. Forth can be compiled, for example. OSes exist - Contiki,
GeckOS, Lunix, etc. ASN.1 is a thing. There are crypto algorithms made
for smaller, slower platforms, usually under the heading of the
Internet of Things. There are people already who find these ways, use
them, make them. They made the videos I watched and web pages I read
(some of these hailed from the 90s, and have aged well).

I took apart a Spaceball from 2003 and found a 6502 inside. (Well, a
Mitsubishi 37450. Same same, except a cursory search reveals only 2500
37450s available in the world, whereas 65C02s can be easily had, and
65C816s if one were to wish.) I've been consumed with the idea of
building it into a computer, one that can be understood down to the
metal (this is one of the principal urges to retrocomputing, I
think). I've read about how, and I probably could if I really
tried. To do it right, I'd need to design a PCB; protoboard may
work. But it had a 10MHz crystal so breadboarding may not work. I'm
just not sure if it would be worth the effort, particularly because
nobody else could learn anything specific from what I did because they
don't have a 37450 chip. So I read more instead. And I don't know what
it should not do, so I don't have any idea of an end to it. And I need
another project like a hole in the head. I still haven't got the right
keyboard yet.

All told, the thoughts I've thought remind me of the difference
between old cars and current cars: you can understand how an old car
works, but it doesn't work as well, and you have to spend more time
thinking about the car and not your destination. This can be enjoyable
and some do enjoy it, but most people just need to go places.

Analogously, I need to easily see and share all my photos, or listen
to all the music I own on all the devices I have. I need that
practical stuff more than I need to impose artistic constraints on my
computing activity. But I also need to escape from the relentless
purposefulness of work sometimes.

Oh, the title. Climate change is happening, income inequality is
widening, and there are those saying that indefinite growth is not a
way to run an economy if we want to leave a habitable planet to our
great-great-grandchildren. Mass surveillance and political
manipulation are happening. I want to find humble ideas of
computing. More decentralized, more resilient, less imperialistic.
