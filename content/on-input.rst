on text-based user interfaces
#############################
:date: 2017-01-19 10:14
:author: jaredj
:category: Uncategorized
:slug: on-input
:status: published

I grew up with Commodore BASIC, command.com, and bash. Somewhere in
there I found Plan 9. A bit of Cisco. A bit of Solaris (sh,
csh). Emacs for the last five or six years. In the past couple of
years at work I've begun using Powershell a great deal, and more and
more of the Linux tools I've used have been written by Red Hat. Also
I've started using BSDs.

Here are my complaints:

 - Red Hat can't decide whether to use subcommands or switches, even
   in the same command.
 - I had an automated Powershell script hang the other day, and it
   took several hours to find out that I had omitted a compulsory
   switch, and Powershell was prompting for a value for that
   parameter. The prompt was sent to nowhere, there was no way to
   provide input, but still Powershell happily waited for an answer.

The problem with Red Hat's tools is that they are manipulating objects
directly, rather than language-based representations of them. This
moves complexity from the description of the object in a text file to
a description of the operation to be done to the object using
command-line parameters. To be sure, it enables easier construction of
GUIs and web UIs, as alternate (who are we kidding, primary) sources
of the same API calls. But it also gives me a lot of things I hate
about PowerShell while taking away what I love about Unix. Perhaps I
could say that more people can speak in these terms, but no one can
utter poetry.
