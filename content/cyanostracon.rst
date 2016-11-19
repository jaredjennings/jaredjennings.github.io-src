cyanostracon
############
:date: 2016-11-02 23:19:35
:author: jaredj
:category: Projects
:slug: cyanostracon
:status: published

`darbrrb <https://github.com/jaredjennings/darbrrb>`_ is
well-developed and well-tested. I've made several backups with it. But
I've grown frustrated with how serial it is. I decided early on to
make it as simple as I could: it calls dar (so to be able to write
down exactly how dar was called inside the backup), dar calls it after
every slice, and before it hands control back to dar, it will run par
to generate archive files, and/or it will burn a completed set of
optical discs.

The opportunity for improvement is that, while par is fast, it could
be running at the same time as dar creates more slices. And, more
interestingly, if multiple Blu-Ray drives exist, multiple discs of a
set could be being burned at once (during a backup) or read at once
(during a restore). But making this possible requires inversion of
control, such that instead of waiting until a thing has finished and
doing the next thing, we can ask for everything to be done that can be
done for now, and when something is done that we can act on, we act on
it, in an event-based fashion.

cyanostracon is the attempt to invert control in this fashion. It's
slow going but it's taking shape, based on David Beazley's `curio
<https://github.com/dabeaz/curio>`_ library. It's not hosted anywhere
yet, but it'll probably go up on GitLab one of these days.

-- Edited to add: `cyanostracon is on GitLab <https://gitlab.com/jaredjennings/cyanostracon>`_.
