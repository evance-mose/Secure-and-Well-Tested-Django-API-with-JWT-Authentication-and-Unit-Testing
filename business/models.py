
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Customer(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
 
    title = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=10, choices= GENDER_CHOICES)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.PROTECT, default=1 )
    created = models.DateTimeField(default= timezone.now)
    status = models.CharField(max_length=10, choices= STATUS_CHOICES, default='draft')

    
    objects = models.Manager()
    published = PublishedManager()


    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers' 
    
    def __str__(self):
        return "{} {}".format(self.name, self.last_name)
