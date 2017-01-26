sagemincer broken
#################
:date: 2017-01-25 23:07
:author: jaredj
:category: Projects
:slug: sagemincer-broken
:status: published

So http://securityrules.info/ is still around, and highly trafficked
by search engine bots—bingbot, Googlebot, AhrefsBot, Baiduspider,
MJ12Bot and BLEXBot. Real people appear to have fetched around 15,000
pages of information about security rules in the past month—around
20 hits per hour on average.

But there is a big problem: it doesn't appear that up-to-date STIGs
are being shown on the site. I expended a great deal of effort to make
sure it would Just Work, without my constant supervision. But there
are problems that block fixing that. To wit:

First, the site is running an old version of sagemincer, and it
appears this has some silly error in it that makes the fetch always
fail under present conditions.

But even if that were fixed, sagemincer takes up 91% of its disk
quota, with its logs just scrubbed. If it were to successfully fetch
new STIGs, it would run out of space. I have a `Trello card
<https://trello.com/c/8a4Gywf6/38-deal-with-space-constraints>`_ about
that, but haven't done anything to fix it.

But even if that were fixed, OpenShift Online is going away some time
soon. sagemincer needs to run in containers instead, but OpenShift
Online next gen isn't in place yet, and will likely cost money when it
is. Other container hosting exists today; using it means doing CI/CD
outside OpenShift, and it will likely also cost money.

I don't want to pay money nor set up ads, and I don't want all of my
cool URIs to fail to resolve either. Grumpf.

Oh also I just read a few blog articles about Luigi, Airflow, and
Pinball, which all seem to be dealing in bigger data than I am; and
LinkedPipes ETL and UnifiedViews, which are about ETLing with RDF but
are too anti-coding. And I read about Kafka—intriguing as it was last
time I looked, but also too big iirc.
