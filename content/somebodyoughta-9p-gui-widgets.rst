Somebodyoughta: 9P + GUI widgets
################################
:date: 2015-01-30 04:15
:author: jaredj
:category: Uncategorized
:tags: somebodyoughta
:slug: somebodyoughta-9p-gui-widgets
:status: published

So `Acme <http://plan9.bell-labs.com/sys/doc/acme.html>`__ exposes its
windows and their contents through 9P. You can easily extend it by
writing programs that mess around with the files it serves. Very neat
idea. Now Inferno also has a lot built on 9P, but it uses Tk for its GUI
widgets. I get it, Tk was small and simple, and their innovations
weren't in GUI design but system design. But I never loved Tk, and it
just isn't so beautifully simple as the rest of Plan 9 and Inferno.

So what if you had a widget toolkit that's a file server? It consumes
the display, keyboard and mouse devices like any window in Plan 9 or (I
think) Inferno, but serves a tree of files and directories corresponding
to widgets, and probably another tree corresponding to events. Rather
than some XML file describing your GUI form, you have a tree of files
and directories. Now designing a form is a matter of mkdir and cat. Then
make a copy of the live widget tree in your project's source somewhere,
to copy back later at runtime. Also, maybe someone could make a widget
server that can talk OpenGL and animate things, so then the
`Hellaphone <https://bitbucket.org/floren/inferno/wiki/Home>`__ could
look like something a smartphone user might want to use. Like, if
someone ported Hellaphone on top of
`libhybris <https://en.wikipedia.org/wiki/Hybris_%28software%29>`__,
they could expose Wayland compositing inside Inferno using Styx.

While I'm coming up with crazy ideas—somebodyoughta take this blog and a
lot of funding, and get college students to implement all this stuff.
Like Jared's Summer of Code or something.
