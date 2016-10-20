# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PIL import Image
from django.db import models


class BillRegion(models.Model):
    title = models.CharField(max_length=50, verbose_name=u'Название',
                             unique=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Bill(models.Model):
    title = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.TextField(max_length=300, verbose_name=u'Описание')
    region = models.ForeignKey('BillRegion', related_name='bills',
                               verbose_name=u'Область')
    contacts = models.TextField(max_length=100, verbose_name=u'Контакты')
    image = models.ImageField(upload_to='bills/img/',
                              verbose_name=u'Картинка', blank=True)
    date_creation = models.DateField(auto_now_add=True, 
                                     verbose_name=u'Дата создания')

    def __unicode__(self):
        return "%s %s" % (self.title, self.region.title)

    class Meta:
        ordering = ['title']

    def save(self, *args, **kwargs):
        super(Bill, self).save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image)
            image.thumbnail((200, 200), Image.ANTIALIAS)
            image.save(self.image.path, 'JPEG', quality=100)