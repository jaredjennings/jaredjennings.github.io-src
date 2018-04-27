xah-fly-keys rough edges
########################
:date: 2018-04-26 18:03
:author: jaredj
:category: Editors

Here's a list of things I want to improve about xah-fly-keys in spring 2018. (In September 2017, I didn't know some things I know now.) To-dos not gripes.

 1. ``s`` does not work like Vi's ``o`` or ``O``, but like Emacs'
    ``C-o``. When I open a line, I want what's on the line I have my
    cursor on to move down a line, not to split a line. I have a
    function that does this but making it happen when I press ``s`` is
    a matter of hacking up ``xah-fly-keys.el``, or waiting for the
    change Xah has said he wants to make, where keymaps are switched
    not rewritten when modes change.

 2. ``c`` does not work like ``x``, in that it does not include the
    newline at the end when run without the mark active (i.e.,
    linewise). Because of this I don't even use ``c``. That leads to
    other problems.

 3. The amount of precision and subtlety devoted to moving is
    different than that devoted to copying or deleting. I *love* the
    ``ijkl``, ``uo``, ``h;``, and other movement keys I haven't
    learned to use. I've rejected ergoemacs in large part because its
    ``M-h`` and ``M-S-h`` are so much worse than ``h`` and ``;``. But
    half the time when I want to delete a word with ``e`` or ``r``, I
    end up nuking half my document instead, because the mark was set,
    which I didn't know about and can't see, and ``e`` deletes the
    region *plus a word*. Also nearly every time I type ``g``, I was not
    trying to delete a paragraph. I think the solution here is to
    learn to use the mark more intentionally. But—

 4. ``e`` and ``r`` do something different if the mark is set, but
    ``x`` and ``c`` only do something different if the mark is
    activated.

To really do this up right, I need to record all my commands and see
what I do most often—i.e., do the same legwork Xah did. The immediate
thing to do with such knowledge would be to move commands around
between keybindings. The deeper thing to do would be to look at
sequences of commands and ask how they could become single
commands. This should include looking at things I do, then undo, and
asking why they didn't work right.

But this amount of introspection about text editing is a level of
detail I don't usually want to descend to. It already takes me too
long to figure out what I really need to say, without also thinking
about how to type it.
