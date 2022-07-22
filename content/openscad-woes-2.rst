OpenSCAD continued musings
##########################
:date: 2018-04-10
:author: jaredj
:category: Keyboards

I've looked at the overly lengthy SCAD code that's being generated to
describe the marshmallowy sides of my keyboard. These sides are
presently described as the Minkowski sum of a sphere with a ribbon
that goes around the edge of the keyboard, differenced with the
Minkowski sum of a smaller sphere with the same ribbon, then with more
stuff cut out of the inside.

I originally made the ribbon by some CSG involving spheres that
approximate the surface of the keys, but this seemed slow and needed
endless tweaks that were not directly related to existing parameters
about the keyboard, and therefore would immediately cease to fit if
anything else were changed. Also I needed to split the sides up into
pieces, but I couldn't think of any way to place the connectors for
the pieces, because I couldn't say, "do all this CSG, use it to find a
point, and place this thing there," and I couldn't calculate where the
point is without copying the set of transforms I was asking OpenSCAD
to do, in Clojure.

These days I make the ribbon by pairwise hulling a bunch of web posts
placed around the outer edges of the keys. (A web post is just a
little toothpick that is web-thickness tall.) Now I look at the SCAD
and it looks like this::

  union () {
    hull () {
      a transform([3.9999999999, 0, 4]) {
        another transform {
          another transform {
            are you starting to get the point {
              no seriously these go six deep {
                bla bla bla {
                  cube([0.1, 0.1, 4])
                }
              }
            }
          }
        }
      }
      the whole caboodle again for another little cube () {}
    }
    the whole hull thing for each pair of posts around the ribbon {}
  }

This is all repeated twice, once to minkowski the bigger sphere, and
once for the smaller. This is why it takes 5MB to describe a
marshmallowy sides shape. And then every time I try to intersect
something with that, in order to attach a connector to it, I'm
describing another marshmallowy sides shape, from scratch.

There are several ways out that I can think of:

  1. Go back to differencing spheres. The unknowns that forced the
     key-placed-ribbon remain.
  2. Define key-place in OpenSCAD. Teach clj-scad to import the manual
     OpenSCAD definition, and to call the defined module.
  3. Achieve some mystical union between functions that transform and
     the matrix math they perform, so that it's equally easy to say
     "key-place this object" and "imagine a point transformed thusly;
     now use it in this OpenSCAD [x,y,z] sort of context."
  4. Pull out libfive again and figure out how to use it, because it
     has a thinner wall between the nice high-level language and the
     language whereby shapes are defined.
