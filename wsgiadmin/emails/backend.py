from constance import config
from os.path import join
from wsgiadmin.core.backend_base import Script
from wsgiadmin.core.utils import get_mail_server


class EmailBackend(object):
    def __init__(self):
        self.script = Script(get_mail_server())

    def install(self, email):
        homedir = join(config.maildir, email.domain.name)
        maildir = join(homedir, email.login)

        self.script.add_cmd("mkdir -p '%s'" % homedir)
        self.script.add_cmd("chown email:email '%s' -R" % homedir)
        # Good for courier, not for dovecot
        #self.script.add_cmd("maildirmake '%s'" % maildir)
        #self.script.add_cmd("chown email:email '%s' -R" % maildir)
        #self.script.add_cmd("maildirmake '%s'" % join(maildir, '.Spam'))
        #self.script.add_cmd("chown email:email '%s' -R" % join(maildir, '.Spam'))
        self.script.add_cmd("mkdir -p '%s'" % maildir)
        self.script.add_cmd("chown email:email '%s' -R" % maildir)

    def commit(self):
        self.script.commit()

    def uninstall(self, email):
        maildir = join(config.maildir, email.domain.name, email.login)
        self.script.add_cmd("rm -rf '%s'" % maildir)

    def uninstall_domain(self, domain):
        for email in domain.email_set.all():
            self.uninstall(email)
        homedir = join(config.maildir, domain.name)
        self.script.add_cmd("rm -rf '%s'" % homedir)
