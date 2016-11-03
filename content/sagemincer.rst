sagemincer
##########
:date: 2014-08-08 02:44
:author: jaredj
:category: Projects, Security
:slug: sagemincer
:status: published

If you've been reading my Compliance at Home series, you'll know that
the DoD releases security guidance in the form of STIGs. They're
downloadable as ZIP files, which contain ZIP files, which contain
checklists written in XCCDF, and stylesheets that can turn the XCCDF
document into HTML. So if I want to talk about one STIG requirement,
say, on this blog, there's no URI that identifies it globally, and no
URL where I can directly browse information about it. So over the last
month I wrote `sagemincer <https://gitlab.com/sagemincer/sagemincer>`__,
which minces security guidance into individually addressable pieces.
There's a copy of it running `here <http://securityrules.info/>`__.
(Here's one requirement: `Keep your Java Runtime Environment
updated <http://securityrules.info/id/A7V-fxHiPC/V-39239>`__.)

EDITED: changed link destinations to new domain; see newer post.

EDITED 2: project moved to GitLab because `Gitorious was to be shut
down <https://about.gitlab.com/2015/03/03/gitlab-acquires-gitorious/>`__;
link updated.
