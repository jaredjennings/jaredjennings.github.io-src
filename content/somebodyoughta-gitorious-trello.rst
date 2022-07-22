Somebodyoughta: GitLab + Trello
###############################
:date: 2015-01-30 04:44
:author: jaredj
:category: Software development
:tags: somebodyoughta
:slug: somebodyoughta-gitorious-trello
:status: published

This is way less pie-in-the-sky than any of the other somebodyoughtas.
Take a weekend and bang it out.

(UPDATED: `GitLab acquires Gitorious; gitorious.org to shut
down <https://about.gitlab.com/2015/03/03/gitlab-acquires-gitorious/>`__.
But GitLab doesn't have a Trello integration either. So the
somebodyoughta materially stands.)

You've probably heard of `GitHub <https://github.com/>`__. It's a site
that hosts Git repositories. The software that runs their site is
fabulous, and proprietary. `Gitorious <https://gitorious.org/>`__ is a
similar Git code hosting site, but the site software is available under
the `AGPLv3 <http://www.gnu.org/licenses/agpl-3.0.html>`__. Trello is a
site that hosts virtual kanban boards, where (if, for example, you are
running a software project) you can make a virtual card for each change
you want to make to your software, add little color swatches to it to
indicate that it's really important or it has to do with subcomponent X,
and move it from list to list (e.g., "Somebodyoughta" to "Working on
it") within the board. So like a bug tracker but with much more wisdom
in its user interface.

So when you make changes to your code, you may want to move a card in
direct response, perhaps from a "Coding" list to a "Ready to test" list
or something. GitHub has `web
hooks <https://developer.github.com/webhooks/>`__, whereby when you push
changes to the repository, GitHub sends an HTTP POST request to a URL of
your choosing, whose body contains data about the changes pushed. Trello
has a well-developed
`API <https://gitorious.org/gitorious/pages/WebHooks>`__ whereby you can
programmatically tell it to, say, move a card from a list to another.
These two aren't exactly the same, so it takes a little code to adapt
between them. Someone has
`written <https://github.com/zanker/github-trello>`__ this code.

Gitorious also has `web
hooks <https://gitorious.org/gitorious/pages/WebHooks>`__. They are
similar but not quite the same, I think. No one has written a
Gitorious-Trello adapter. Somebodyoughta.
