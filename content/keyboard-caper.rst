the keyboard caper
##################
:date: 2017-11-04 23:18
:author: jaredj
:category: Projects

The editor caper continues, kind-of. I'm pretty settled on
xah-fly-keys now, although it still doesn't have C-k. I found out the
side arrow keys move you from search result to search result. This is
a jarring inconsistency with the ijkl keys. And in the few cases when
I've quickly dropped into vi to edit something, ijkl and f/CapsLock
vs. hjkl and a/Esc have gotten to me. But that's not why we're here!

I figured out why my wrists hurt: (1) I was using my netbook on the
bus. The Dell Latitude 2120 has an undersized keyboard, with keys
harder to press than most laptops. Using a keyboard on my lap appears
to be a bad idea at this time in my life; using a small keyboard makes
me twist my wrists more, and using one that takes more force than most
magnifies the damage. (2) I was using a keyboard in front of my laptop
at work, because I got a new laptop that didn't have Home and End
keys. This made me point my forearms inward, and my wrists back
out. Now I'm not typing anything on the bus (sorry, cyanostracon
project! and andy!) and dealing with the Fn+Left and Fn+Right that are
my Home and End keys. And because I'm silly...

I started to think about keyboards. I started to look at keyboards. I
started to read about keyboards. Xah Lee has a good deal to say about
them, and r/mechanicalkeyboards and r/mechmarket. Xah talked about the
Kinesis Advantage, and, not wanting to lay out a bunch of money for an
ergonomic keyboard, I thought I'd figure out a way to make one
myself. I found the `Dactyl keyboard
<https://github.com/adereth/dactyl-keyboard>`_, and the `Dactyl
Manuform keyboard <https://github.com/tshort/dactyl-keyboard>`_, and
the `Manuform keyboard <https://github.com/jeffgran/ManuForm>`_, which
hold out exactly this prospect. I set out to make a Dactyl. I figured
out I'd pay $250 or so to get the case printed by Shapeways, and
something less but still repugnant to get the case printed by
3dlabs. I joined `hackPittsburgh <https://hackpgh.org/>`_ to get
access to a 3-D printer. I bought some `keycaps
<https://pimpmykeyboard.com/sa-ice-cap-keyset/>`_. Among the many I
got, there weren't enough 2u keys, so I bought some of those.

And then I tried to print out the keyboard case. It's bigger than the
print volume of any of the printers they have. I asked around and
found out about Voodoo Manufacturing, which would print my keyboard
case for something like $120. Very nice! But still too expensive to
try something, think better of it, and try something new.

Now, all the three keyboards above are shared and updated in the form
of programs that output CAD stuff which you can turn into STL files
which you can turn into Gcode which you can tell to a printer and turn
into plastic. When the keycaps weren't all the right size I needed, I
thought about modifying one of the designs. But despite being a
program, it's still not quite at the level of abstraction I'd like to
be modifying. The Dactyl is written in Clojure, which outputs OpenSCAD
language, which OpenSCAD turns into an STL. Slowly. Five minutes per
iteration. This lacks quality. `OpenSCAD issue 237
<https://github.com/openscad/openscad/issues/237>_` says turn fa, fs
or fn down.
