for PAR1
########
:date: 2016-02-07 05:42
:author: jaredj
:category: Backup
:tags: par, par1, par2
:slug: for-par1
:status: published

I looked in the source of parchive (which is only like 3500 lines of
code to par2cmdline's 13500 or so) and didn't find any evidence of the
flawed math that was in the original RS tutorial. I don't think parchive
is flawed at this point.

And it's five and a half times faster than par2cmdline!! As packaged by
Debian, which means probably no whiz-bang optimizations! Bump turbo
codes, bump making my own file format, it works here and now, GPU or no.
Case closed, for now at least.

See also `darbrrb issue
2 <https://github.com/jaredjennings/darbrrb/issues/2>`__, which is where
I should have written all this mess. Oh, well.
