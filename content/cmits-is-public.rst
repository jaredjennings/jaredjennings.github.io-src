CMITS is public!
################
:date: 2015-03-24 02:45
:author: jaredj
:category: Compliance at home, Security
:slug: cmits-is-public
:status: published

Configuration Management for Information Technology Systems (CMITS) is a
melding of Puppet, LaTeX and my own scripts that makes compliance with
hundreds of security requirements maintainable for me at work. And I've
obtained permission to release it. The initial release is made at
https://github.com/afseo/cmits, in the "public domain" as defined by
copyright law; forthwith I have made my own forks of each of its pieces,
and placed them under various open-source licenses. In these forks I've
applied some effort to make the unified policy document build properly
at home and make more sense in a public context.

There's a Python piece, and two LaTeX pieces, and a big ball of Puppet
code that according to modern Puppet practices should be at least fifty
pieces. Each of these languages has a canonical repository: PyPI, CTAN,
and the Puppet Forge, respectively. As of this writing, none of the code
has made its way to those places. So if you want to try it out, the
first thing to do is get the `pre-built unified policy document for the
example
policy <https://github.com/jaredjennings/cmits/raw/master/build-products/cmits-example.pdf>`__,
read, and marvel. Then if you want to build your own (see also
prerequisites in the various READMEs):

#. git clone https://github.com/jaredjennings/latex-cyber
#. (cd latex-cyber; make && make install)
#. git clone https://github.com/jaredjennings/latex-cybercic
#. (cd latex-cybercic; make && make install)
#. git clone https://github.com/jaredjennings/shaney
#. (cd shaney; python setup.py install)
#. git clone https://github.com/jaredjennings/cmits
#. cd cmits/cmits-example/unified-policy-document
#. make
