from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    # Single category, which will be assigned to blog entries
    name = models.CharField(_('Name'), max_length=64)
    description = models.TextField(_('Description'), blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Categories')


class Entry(models.Model):
    # A blog post with basic information
    editor = models.ForeignKey('auth.User', related_name='entries')
    title = models.CharField(_('Entry Title'), max_length=256)
    text = models.TextField(_('Content'))
    categories = models.ManyToManyField(Category)

    def __unicode__(self):
        return _('{0} (by {1})').format(self.title, self.editor.username)

    class Meta:
        verbose_name_plural = _('Entries')