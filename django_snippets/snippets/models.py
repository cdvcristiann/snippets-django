#from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from django.db.models.signals import pre_save

class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    slug = models.CharField(max_length=50, null=True, blank=True, verbose_name='Slug')


    def __str__(self):
        return self.slug


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Language, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Lenguaje'
        verbose_name_plural = 'Lenguajes'
        ordering = ['id']


class Snippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,  null=True, blank=True, verbose_name='Usuario')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, verbose_name='Nombre')
    description = models.TextField()
    snippet = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.PROTECT, verbose_name='Lenguaje')
    public = models.BooleanField(default = False)
    slug = models.CharField(max_length=50, null=True, blank=True, verbose_name='Slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Snippet'
        verbose_name_plural = 'Snippets'
        ordering = ['id']