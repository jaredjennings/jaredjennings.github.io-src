the editor caper
################
:date: 2017-09-13 22:17
:author: jaredj
:category: Commentary

For twelve years or so, I used Vim. Then, at work, I decided to try
Emacs for the fifth time or so, and it stuck, particularly when I
managed to teach find-file-at-point how to find the file defining a
given Puppet class, when my cursor was on the class's name. At work, I
use Emacs on Windows, frequently using TRAMP to edit files over ssh on
Linux or BSD boxen. At home, I use Emacs on Linux.

And so it has been, until my wrists began to hurt at the same time
that I began to feel adventurous.

Every once in a while, I go on a bender, and decide to try to upend my
entire computing environment. I try out Plan 9, Haiku, NetBSD. A time
or two ago I read the whole Rust book; this time I'm threatening to
learn Go. But I started to earnestly try editors again.

First I got Gvim for Windows. Same problems as always: it isn't really
happening in a terminal, and it isn't really happening on a Linux box,
and to change things about it you have to use vimscript
*shudder*. Editing files well in any vi-based editor is a dance
between being in the editor and outside the editor, between using the
editor's facilities and using those of the operating system and
shell. And Vim still expects you to save the file you're in before
switching buffers. Drives me nuts!

Then I got Acme-SAC. Same problems as always: I never have a mouse
with three actual buttons, and it can only edit files that live on a
lettered drive, not a UNC path. I got a little farther into it this
time, and wrote a couple of little scripts to use as commands. But the
way you do this is by typing their names in the label of a window, and
the whole label was always taken up with the full pathname of the
file—both at work and at home. It's like acme is made for editing
files with really short path elements, like /n/p/src/9/cmd/ls.c or
something. And there's the tabs position in the spaces-vs-tabs war
that is baked into acme.

I tried sam, which doesn't depend as much on external utilities,
synthetic filesystems, and the like as Acme does. But nobody's ported
it to Windows quite as well as Acme-SAC, much less any better.

Then I went back to Emacs, but got ergoemacs. This was not bad, but it
was meant to defend against Emacs pinky, when half the time I use the
edge of my palm to press Ctrl. It's nearly harder than that to fold up
my thumb to use Alt all the time. And I never got the hang of the
colors on the cheat sheet. These gripes are weak sauce, and I could
come back to ergoemacs.

Then I found xah-fly-keys. This is a modal set of keybindings for
Emacs, that is, the keybindings consist of pressing keys in succession
rather than holding down modifier keys. It's quite good, quite good. I
like the movement with ijkl, u, o, h and ;. If I were to rebind my
Caps Lock to Home to go into command mode like Xah recommends, it
would really be great, but Alt-Space is already much niftier than
Esc. Problems: There are some keys that self-insert in command
mode. This is evil. It actively fools me when I'm not sure which mode
I'm in. Also the primitives leave something to be desired. Two things
happened here: one, I found out that while Xah paid a good deal of
attention to which commands are most often used, he also made new
editing primitives, which don't seem to match my tasks very
well. (Where's C-k?) When editing modally my mind thinks in vi: I want
to delete the next 5 lines, for example, d5d. But xah-fly-keys doesn't
have the same command-howmany-movement kind of thing going on as vi,
it just uses the same mark-then-do-something paradigm as Emacs, and I
miss it sorely. And marking, while it works right in a graphical
Emacs, doesn't always work right on the terminal. And searching! You
type 'n' in command mode to search, in this mode where allegedly you
never have to use Ctrl, but then how do you get to the next
occurrence? You have to use Ctrl-S! Awful! And whatever special keys
you use in some buffers, you usually have to go into insert mode to
convey properly. Like dired, or help, or so on.

Let me say here that I listened to the `Emacs Chat episode with Xah
Lee <http://emacslife.com/emacs-chats/chat-xah-lee.html>`_, and I'm
sure he would say if I don't like his editing primitives, that's not
his problem: he was just trying to scratch his own itch, and the real
message is that users of Emacs should more freely customize their
editor.

Then I got evil. This is vi for emacs done properly. I've tried viper
a couple of times before, and the moment I found it didn't have ":b
otherfileimworkingon.txt" to switch buffers, I indignantly dropped
it. evil gets this and so many other things right. Keybindings for
dired and help work properly in command mode. Colon both lets me do vi
commands and M-x commands—beautiful! But when I'm on the terminal, Esc
somehow doesn't mean "move from insert to command mode," it means
"maybe he meant to press Meta-something, wait for a second and see."
Then when I press k to go up a line, Emacs says, "aha Esc-k means M-k,
and so I'll kill a paragraph." Agh!

Something that's come up a couple times here is "when I'm on the
terminal." I do still use terminals, and care that they work
right. Some key combos don't work right on terminals. C-/ for undo,
for example, doesn't work. C-- does. Meta doesn't always work, thus
the Esc thing. I have legitimately used Esc instead of Alt before
because my terminal couldn't handle it. It was Kermit on a 486 DOS
laptop. And in 2009, not 1993! Er, get off my lawn.

So Plan 9, being built for a graphical display but still primarily
meant for dealing with text, is a thing I really like. I just don't
have a three-button mouse anywhere, and don't have a mouse
everywhere. But having no application code for dealing with command
history, scrolling back output, command-line editing, *because it's
all done by the OS and all done the same way*, is so compelling.

I even tried Notepad++ a bit. But it's too Windowsy. Dialog boxes
everywhere, eugh.

I found other editors like Kilo. I'm inspired by the thesis that text
editing is not complicated and we don't all need to use text editors
that are forty years old, particularly after reading Xah Lee's history
of how the vi and emacs keybindings came to be. But part of the
runtime of these forty-year-old editors is in my brain. vi and emacs
have shaped the way I think about manipulating text.

