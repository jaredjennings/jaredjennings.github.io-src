libfive cool-off
################
:date: 2018-04-13 17:39
:author: jaredj
:category: Projects

libfive doesn't have a hull nor minkowski operation. The Dactyl
depends hravily on the hull operation; my marshmallowy sides depend on
minkowski. The sides can probably be reformulated, and perhaps even
improved; and there is at least a `paper
<http://hyperfun.org/Mink.pdf>`_ about it (if the link dies, that
reference is: Pasko A., Okunev O., Savchenko V., “Minkowski sums of
point sets defined by inequalities”, Computers and Mathematics with
Applications, Elsevier Science, vol. 45, No. 10/11, 2003,
pp. 1479-1487.) But it says the operation is very slow, and it gets
into details of how to implement it satisfactorily that I think have
some interference with how libfive is implemented. Whether
constructive or destructive, I don't know.

The reason I wanted to use libfive, really, was not that it's new, nor
that f-rep is so much cooler than stodgy old b-rep, but that it isn't
made out of Java and might not take ten seconds to start every
time. But at this point the work necessary for libfive to render a
Dactyl-alike, whether by adding operations to libfive or by
reformulating the keyboard, appears to exceed the work necessary to
make Clojure somehow emit a tractable OpenSCAD model, so back to
Clojure for the moment.
