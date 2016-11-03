Somebodyoughta: A secret sharing app
####################################
:date: 2014-10-01 04:38
:author: jaredj
:category: Security, Somebody Oughta
:slug: a-secret-sharing-app
:status: published

I've recently read about secret-sharing protocols, where by means of
mathematics some secret bits can be distributed among some number of
people such that reconstructing the secret requires some size of quorum.
For example, say I've built a successful drink company. The recipe for
the drink is of course secret. I apply this protocol and it splits the
recipe into six pieces, which I give to my closest friends. Four or more
of the pieces will suffice to recreate the recipe, but less than four
will not. (In particular, one piece on its own does not divulge any of
the secret.)

Somebodyoughta make an app for this. It would be insecure, because it's
on mobile devices always connected to the internet, but it would also be
`fun <http://www.amazon.com/dp/0860201678>`__. A file downloaded or
typed in contains the secret message; the pieces are transmitted to the
devices of the trustees, by NFC or maybe QR code; when it's time to
reconstruct the secret, at a solemn meeting one of the trustees bumps
each other trustee's phone screen, and then the secret appears.
