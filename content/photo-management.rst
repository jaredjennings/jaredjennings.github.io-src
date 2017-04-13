photo management
################
:date: 2017-04-12 22:24
:author: jaredj
:category: Projects
:slug: photo-management
:status: published

FreeBSD jails are not nearly so glamorous as OCI/Docker
containers. FreeBSD jail statically assigned IP addresses are not
nearly so glamorous as CNI. But it's been like one week and I have a
PHP/MySQL app up inside a FreeBSD jail with IPv6, where it took me
three weeks or so (check old blog post dates) of noodling about with
CoreOS to figure out it wasn't going to work for me in the way I
wanted.

Lychee is a photo gallery application. It has a snazzy website. By
installing it and importing 1000 photos into it, I found these things:

 * It can import 1000 photos in, like, 30 or 40 minutes.
 * It's not really snappy with 600 photos in a single gallery.
 * It shows names of folders and files fairly prominently.
 * These two mean that it expects you to have organized your photos already.
 * It seems like the goal is to pick some photos and make them publicly available.
 * It doesn't have a progress bar for the import.

I looked at digital asset management systems; several exist that are
open-source, mostly made in Europe, and some of those even have
working websites. They are about helping you choose things to publish,
not managing everything you have. And there was one to help you curate
digital collections—sort of the case where you are a museum in
possession of physical objects, you take some pictures of each, and
you want to create a web experience analogous to a room in your
museum. This, too, assumed the pictures I have to be more topical and
organized than they are.

I'm getting into another crazy mood, where I want to pick up and use
things that are popularly rejected, like NetBSD, Enyo and RDF, and
write impractically large things, like a web-based photo manager. Then
again I just looked through Bootstrap, jQuery, and AngularJS photo
gallery plugins, and there's stuff there, while the entire Enyo
project hasn't said anything for months.
