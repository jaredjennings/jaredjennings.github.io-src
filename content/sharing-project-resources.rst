Sharing project resources
#########################
:date: 2022-08-03 23:52
:author: jaredj
:category: Maintainership
:tags: thehive, security

Everything I've read and watched about being a project maintainer says
to plan for succession: meaning, start thinking about what the next
maintainer will need, as soon as you begin being the maintainer.

A project based around open-source code needs a place to put the code,
possibly some resources for automatically building the code, a place
where the documentation can be hosted, and a place where people can
communicate. Without getting too far into detail, these things can
sometimes be had for free, but someone needs to manage them, and that
someone needs to authenticate themselves.

So the first thing the next maintainer will need is access to all
those resources. Where they are hosted by someone else (e.g. GitHub),
often an organization or team can be constructed; but perhaps not in
every case. The project's resources must be listed, and the list must
be maintained as changes happen. And passwords may need to be
shared. (Maybe this premise is flawed, but I just did a bunch of
reading and dangit I'm going to tell you what I found.)

One way to share passwords is with a password manager made for
multiple people. The one I think of is `BitWarden
<https://bitwarden.com/>`_. But the version hosted by BitWarden could
start `costing money <https://bitwarden.com/pricing/>`_, a can of
worms I don't want to open. Standing up an `instance for the project
<https://bitwarden.com/help/install-on-premise-linux/>`_ is itself
free of charge, but it requires access and sharing of some of the very
project resource passwords that would need to be stored inside the
tool. That's no good.

`KeePassXC <https://keepassxc.org/>`_ keeps secrets in a file. Anyone
can get and use the software, across platforms. Perhaps I could just
put all the project secrets in a KeePassXC database. I could even make
the file easy to get at, because it's encrypted with a good password
and you can even lock it down to a hardware key.

There are several problems there. I can't plug my present hardware key
into my phone (which, so far, I trust enough to do this sort of thing
with). I can't set a backup key, so if I lose my hardware key, the
database is permanently inaccessible. (I don't see an issue in the
KeePassXC project about this.) I can't use one of several passphrases;
it's just the one, really. And if my database is shared widely, many
people could see when it changed last, and anything less than a
perfect cadence of regular password changes would be easy to
detect.

There was `a KeePassXC issue
<https://github.com/keepassxreboot/keepassxc/issues/7232>`_ where
someone wanted to encrypt a KeePass key file to several recipients'
keys using PKCS#7; each team member would have a PKCS#11 smartcard,
which would decrypt the key file, which would then be used to decrypt
the KeePass database itself. Support for directly decrypting the
database with `PKCS#11 devices
<https://github.com/keepassxreboot/keepassxc/issues/255>`_ has also
been requested. Neither of these issues have yet resulted in released
KeePassXC features yet, though.

Along the way of the PKCS#11 ticket, someone figured out you can't do
OATH HOTP nor TOTP to decrypt the database, because validating a code
requires having a plaintext copy of the same secret that the token
knows. And apparently the HMAC-SHA256 challenge-response protocol
currently supported by KeePassXC is specific to YubiKey and `OnlyKey
<https://github.com/keepassxreboot/keepassxc/issues/2064>`_, not an
`industry standard
<https://github.com/keepassxreboot/keepassxc/issues/3560>`_. I am a
satisfied YubiKey customer, but I don't want to force others to
be. Besides the backup token thing.

Security vulnerability reporting is going to require OpenPGP (to a key
shared between maintainers, right?...), and artifact signing may well
require OpenPGP too. I think someone asked to be able to unlock their
KeePassXC database using GnuPG, but the answer came back that this
couldn't be done portably. That's fair.

BitWarden and KeePass are two alternatives, and I don't think either
is really satisfactory. But the up-to-date list of project
infrastructure is more important than a password-sharing solution for
the ages, and this meditation is probably premature optimization.
