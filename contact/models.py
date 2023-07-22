from django.db import models
from core.models import AbstractModel

# Create your models here.

class Message(AbstractModel):
    name = models.CharField(
        default='',
        max_length=254,
        blank=True,
        verbose_name='Name',
        help_text='',
    )
    email = models.EmailField(
        default='',
        max_length=254,
        blank=True,
        verbose_name='Email',
        help_text='',
    )
    subject = models.CharField(
        default='',
        max_length=254,
        blank=True,
        verbose_name='Subject',
        help_text='',
    )
    message = models.TextField(
        default='',
        blank=True,
        verbose_name='Message',
        help_text='',
    )

    def __str__(self):
        return f"Message: {self.name}"

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('name',)

class ContactAreaInfo(AbstractModel):
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
        verbose_name='Order',
        help_text='',
    )
    title = models.CharField(
        default='',
        max_length=254,
        blank=True,
        verbose_name='Title',
        help_text='',
    )
    description = models.CharField(
        default='',
        max_length=254,
        blank=True,
        verbose_name='Description',
        help_text='',
    )
    icon = models.CharField(
        default='',
        max_length=254,
        blank=True,
        verbose_name='Icon',
        help_text='',
    )
    link = models.CharField(
        default='',
        blank=True,
        verbose_name='Link',
        help_text='',
    )

    def __str__(self):
        return f"Contact Area Info: {self.title}"

    class Meta:
        verbose_name = 'Contact Area Info'
        verbose_name_plural = 'Contact Area Infos'
        ordering = ('order',)