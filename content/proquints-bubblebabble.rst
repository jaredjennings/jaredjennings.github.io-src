proquints vs. bubblebabble
##########################
:date: 2017-04-21 22:50
:author: jaredj
:category: Commentary
:slug: proquints-bubblebabble
:status: published

The `Bubble Babble encoding <http://wiki.yak.net/589>`_, due to Antti
Huima, was invented in 2000. It has six vowels and seventeen
consonants, and checksums built in so you can tell whether a purported
Bubble Babble string is valid or not. A Bubble Babble string always
begins and ends with 'x'. This encoding is used in OpenSSH when you
``ssh-keygen -l -B``.

The scheme of `proquints <https://arxiv.org/html/0901.4016>`_
("PRO-nounceable QUINT-uplets") was introduced in 2009 by Daniel
Shawcross Wilkerson. This scheme has four vowels, sixteen consonants,
and no checksums. It takes more linguistics into account, avoiding
homophones; it avoids the use of the character 'x', on account of its
preexisting use to denote hexadecimal numbers. It is suggested that a
proquint string start with '0q-'. Proquints are used in `Upspin
<https://upspin.io>`_.

There's a pretty good `Hacker News thread
<https://news.ycombinator.com/item?id=8751302>`_ mentioning proquints
and also Abbrase (`from rmmh <http://rmmh.github.io/abbrase/>`_, `a
fork from bcaller <http://bcaller.github.io/abbrase/>`_).
