sagemincer updates
##################
:date: 2014-09-27 21:43
:author: jaredj
:category: Security
:slug: sagemincer-updates
:status: published

When first released,
`sagemincer <https://gitlab.com/sagemincer/sagemincer>`__ was slow.
Like, thirty seconds to load a page slow. After a bunch of changes, now
it's fast enough to be far prouder of. Also I got a new domain for it,
`securityrules.info <http://securityrules.info/>`__.

The way it got faster was this: I stopped trying to fetch all the
triples I thought I'd need from the triplestore (4store) using a
CONSTRUCT query, and parse them into a graph model (``rdflib.Graph``).
The step where rdflib parsed 4store's output was very slow. Now
sagemincer uses SELECT queries with JSON output format, and parses them
into dictionaries and lists. It's much faster, but it no longer uses
``rdflib.Graph``, so anything that builds on rdflib (e.g. the only
Python reasoner I've found, FuXi) is out of the picture now. This means
I'm using the flexibility of expression RDF offers (data is shaped like
an arbitrary directed graph, not only a tree or table) but failing to
take advantage of its ability to encode domain expertise using RDFS or
OWL and inference.

EDITED: project source code moved to GitLab.
