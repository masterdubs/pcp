import json
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

CAPABILITIES = [(x, x) for x in ("python", "php", "phpfpm", "mail", "static", "load_balancer", "ns_primary", "ns_secondary", "native", "virt", "mysql", "pgsql")]
OSS = (
    ("debian6", "Debian 6.0"),
    ("debian7", "Debian 7.0"),
    ("archlinux", "Arch Linux"),
)


class Capability(models.Model):
    name = models.CharField(_("Capability"), max_length=32, choices=CAPABILITIES)
    #config = models.TextField(_("Config for capability"), help_text=_("Use docs for details"))

    def __unicode__(self):
        return unicode(self.__str__())

    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(_("Name"), max_length=128)
    priority = models.IntegerField(_("Priority"), default=5, choices=[(x, x) for x in range(1, 11)], help_text=_("Lower is higher"))
    domain = models.CharField(_("Domain"), max_length=128)
    ip = models.CharField(_("IP address"), default="127.0.0.1", max_length=64, blank=True, null=True)
    ipv6 = models.CharField(_("IPv6 address"), default="::1", max_length=64, blank=True, null=True)
    ssh_port = models.IntegerField(_("SSH Port"), default=22)
    os = models.CharField(_("Operating system"), max_length=64, default="debian6", choices=OSS)
    key = models.TextField(_("API key"), null=True, blank=True)
    capabilities = models.ManyToManyField(Capability, verbose_name=_("Capabilities"), null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)
    hide = models.BooleanField(_("Hide in app server field"), default=False)

    user = models.ForeignKey(User, blank=True, null=True)

    @property
    def capabilities_str(self):
        return ", ".join([x.name for x in self.capabilities.all()])

    @property
    def libvirt_url(self):
        return "qemu+ssh://%s/system" % self.ssh

    @property
    def ssh(self):
        return "root@%s:%d" % (self.ip, self.ssh_port)

    @property
    def ssh_cmd(self):
        return "root@%s -p %d" % (self.ip, self.ssh_port)

    def __unicode__(self):
        if self.description:
            return u"%s (%s)" % (self.name, self.description)
        else:
            return u"%s" % self.name

    class Meta:
        ordering = ("priority", )


class PythonInterpreter(models.Model):
    server = models.ForeignKey(Server)
    name = models.CharField(_("Python name/version"), max_length=128)
    cmd = models.CharField(_("Path to python binary"), max_length=128)
    virtualenv = models.CharField(_("Path to virtualenv binary"), max_length=128)
    priority = models.IntegerField(_("Priority"), default=5, choices=[(x, x) for x in range(1, 11)], help_text=_("Lower is higher"))

    def __unicode__(self):
        return unicode("%s on %s" % (self.name, self.server.name))

    class Meta:
        ordering = ("priority", )


class Log(models.Model):
    date = models.DateField(_("Date"), auto_now_add=True)
    content = models.TextField(_("Messages"))

    def get_json(self):
        return json.loads(self.content)

    def __unicode__(self):
        return "Log with id %d" % self.id


class CommandLog(models.Model):
    date = models.DateTimeField(_("Date"), auto_now_add=True)
    server = models.ForeignKey(Server, verbose_name=_("Server"))
    command = models.CharField(_("Command"), max_length=512)
    execute_user = models.CharField(_("Execute user/Owner of file"), max_length=128, default="root")
    stdin = models.TextField(_("Stdin"), null=True, blank=True)
    rm_stdin = models.BooleanField(_("Remove stdin after process"), default=False)
    result_stdout = models.TextField(_("Stdout"), null=True, blank=True)
    result_stderr = models.TextField(_("Stderr"), null=True, blank=True)
    status_code = models.IntegerField(_("Return code"), null=True, blank=True)
    processed = models.BooleanField(_("Processed"), default=False)

    def __unicode__(self):
        return self.command
