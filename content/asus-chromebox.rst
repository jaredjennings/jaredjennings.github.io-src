Asus Chromebox CN60
###################
:date: 2021-06-27 22:17
:author: jaredj
:category: Projects

I'm trying to split my IT estate across two floors of my house. The
present plan for that entails some kind of low-powered device
upstairs, and the muscle in the basement.

I found an Asus mini PC with an Intel Core i3, 8 GB RAM, and two video
outputs, for cheaper than a Raspberry Pi 4, considering the case and
SSD I'd need for the Pi 4. I was waffling about it. Then I found an
Asus Chromebox with an Intel Core i3, 4 GB RAM, a 16GB SSD, and two
video outputs, for cheaper than the Pi 4. I bit. For that price I
could afford to be wrong.

So far I've found that even Chromeboxes with x86 processors are not
quite PCs in the sense I expected, and it's all to do with what
happens at boot time. I did manage to install the TianoCore-based
MrChromebox UEFI firmware, and I'm able to start executing all sorts
of OSes that have EFI bootloaders. But not nearly all of them end up
working. Enough experiences have accumulated that I need to dump them
here.

9front "MIT FRUCHTGESCHMACK"
   I had to unplug and replug the thumbdrive for the installer to
   be able to find it, and there are some odd messages to do with the
   mouse during boot, but graphics, input, storage and networking do
   seem to work. I'm pretty sure nothing is optimized though. I run
   a lot of CAD lately; both CGAL (underneath OpenSCAD) and OpenCascade
   (underneath FreeCAD, to say nothing of Qt) require C++, which is
   nowhere to be found in the Plan 9 universe, and I'm not certain
   that the VNC viewer will push pixels fast enough for me. Also the
   ssh client appears not to support public keys.

Haiku Beta 2
   Boot screen with light-up icons shows; they fly by, but then the
   machine reboots.
   
NetBSD 9.2, FreeBSD 13.0, Dragonfly 6.0
   All three of these hang at boot just after showing "EFI framebuffer
   information." It appears there is `a FreeBSD bug filed about it
   <https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=209821>`_, and even
   a patch under review. If I had stronger build-fu, I could build a
   FreeBSD install thumbdrive with the patched loader.

OpenBSD 6.9
   Downloaded the USB image; didn't try it. I think I don't like Theo.

Debian GNU/Linux 10.10
   Installer boots nicely. Network card (rtl8169 was it?) requires
   nonfree firmware. Wait, on a second install it didn't require the
   firmware?? Anyway ChromeOS is Linux, so this machine will run Linux
   well.

Fedora
   I haven't liked the way Red Hat does open-source software for a
   while. They start or join projects that make the software that the
   company needs for its products, and they make the code grow, but
   maybe not the project. The result is a piece of software with
   poorly stated goals, little or no useful documentation, and a weak
   community. It's only really useful and dependable when you buy the
   Red Hat product. And it's summarily dropped the moment the
   company's strategy no longer includes it. Fine decisions for a
   company to make—maybe even not as bad as some other open-source
   strip mining that goes on—but I'm not inclined to help them.

Slackware
   Last released in 2016, bless them.
