OpenSCAD woes
#############
:date: 2018-04-07
:author: jaredj
:category: Keyboards

I've gotten to the point in my `keyboard building
<https://github.com/jaredjennings/dactyl-keyboard>`_ (the real action
is happening in branches other than master) where I want to connect
the new cool sides I've made to the frame of the keyboard. No sweat,
right? Just come up with a cool connector, draw a sort of cone out
from that connector intersecting the cool curvy side, intersect the
cool curvy side with the cone, and hull that intersection to the
beginning of the connector, right?

Uh-oh. The OpenSCAD output resulting from those cool sides somehow
amounts to like 5MB. And every time I want to intersect those cool
sides with something, the entire shape is reiterated in the OpenSCAD
output. So now it's 35MB of OpenSCAD code, and it takes up gigabytes
of RAM just seemingly to parse it.

With every large setback in this project, I've looked aside: maybe I
should be writing this in Python instead. Maybe I should be writing it
in OpenSCAD instead—it can't be quite as bad as Matt Adereth said,
right?—or perhaps that libfive thing that the fstl author wrote. But
every time I've realized how much work it would be to start over from
first principles, and if there were ever a community for this thing
how much smaller it would be for not being a branch of The Dactyl
Keyboard. I've also found that most other things besides OpenSCAD that
let you describe a 3D object with code and render it to polygons are
immature, unmaintained, or both.

In this particular case, though, writing raw OpenSCAD wouldn't help: you can't say ::

  x = this cool object;
  intersection() { x; some other thing; }
  intersection() { x; some third thing; }

OpenSCAD (afaict) doesn't let you do anything with an object other
than state it exists. Now you can make a module, so you could say ::

  intersection() { this_cool_object(); some other thing; }
  intersection() { this_cool_object(); some third thing; }

but now you are making multiples of ``this_cool_object``, and that is
the problem. I could try to approximate the local shape of the cool
object with something simpler, but it would be tricky and error-prone.
