libfive
#######
:date: 2018-04-10
:author: jaredj
:category: Keyboards

So earlier I got `libfive <https://github.com/libfive/libfive>`_ and
built and installed it, and the libfive Studio segfaulted. And then
updates caused the Studio to work. But I do a lot of my work through
Termius and VNC on my phone while riding the bus, and Studio has a
small font with low contrast, and I want to edit my text with Emacs
anyway. I rejected libfive earlier thinking it wouldn't be able to
make an STL file with sharp corners; but it's smarter than all that.

I've set out to make libfive work for me this time in order to reduce
the distance between transforming objects and deriving points. I think
that boundary still exists but at least it's all written in the same
language. Also I've been annoyed at how slowly Clojure's repl starts
up (But you shouldn't start it every time, you should leave it
running! you say. But I'm not used to old definitions sticking around
when I rename a function and forget to rename all the calls to it. So
I decided to start with a clean slate every time.) and runs my
code. Also dragging in the entire JVM just to write a text
file... eh. Also the EPL is incompatible with the GPL. Also the way
clj-scad is writing OpenSCAD code causes it to balloon in size in the
particular case I'm throwing at it.

(Oh, before I forget—the reason I wanted to derive points was so I
could make more math happen in Clojure and less in OpenSCAD, by
deriving points and stitching them together into polyhedra. This would
speed up the OpenSCAD rendering by a lot, but slow down the Clojure
run. Eh, perhaps it would be faster than writing the OpenSCAD code to
piecewise hull a lot of cubes with eight transforms on each one.)

So, there's not that much documentation for libfive usage outside the
Studio. I figured out how to make my run-of-the-mill Guile 2.2.3
install render an STL file, and here it is.

 1. Get and build libfive. (This is documented by the libfive project.)
 2. Install libfive. (You may not have to do this but it's what I did.)
 3. Make a note of the path to libfive-guile.so, and the directory
    where shapes.scm is found. Mine were at
    ``/usr/local/lib/libfive-guile.so`` and
    ``/home/jaredj/libfive/libfive/bind``. Call these GUILESO and
    SHAPESPD.
 4. cd to SHAPESPD; ``ln -s . libfive``. This is so that when SHAPESPD
    is added to your Guile ``%load-path`` and you ``(use-module
    (libfive foo))`` and Guile looks for ``SHAPESPD/libfive/foo.scm``
    it will find it.
 5. In SHAPESPD, write a file ``kernel.scm`` with the following
    contents::

      (define-module (libfive kernel))
      (load-extension "GUILESO" "scm_init_libfive_modules")
 
 6. Write a file ``cube.scm`` that says this::

      (add-to-load-path "/home/jaredj/libfive/libfive/bind")
      (define-module (cube)
      #:use-module (libfive kernel)
      #:use-module (libfive shapes)
      #:use-module (libfive transforms)
      #:use-module (libfive vec))

      (shape->mesh (box-centered #[1 1 1]) "cube.stl" 10 '((-2 . 2) (-2 . 2) (-2 . 2)))

 7. ``guile cube.scm``


Along the way, I figured out the arrow macros from Clojure, written in Guile::

  (define-syntax ->
    (syntax-rules ()
      ((_ x) x)
      ((_ x (f a ...)) (f x a ...))
      ((_ x (f a ...) (g b ...) ...) (-> (f x a ...) (g b ...) ...))))

  (define-syntax ->>
    (syntax-rules ()
      ((_ x) x)
      ((_ x (f ...)) (f ... x))
      ((_ x (f ...) (g ...) ...) (->> (f ... x) (g ...) ...))))
