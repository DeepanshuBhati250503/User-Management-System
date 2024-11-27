from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    roles = models.ManyToManyField('Role', blank=True, related_name='users', help_text='Roles assigned to this user.')




    
class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField('auth.Permission', blank=True)
    priority = models.IntegerField(default=0)  # Add priority field

    def __str__(self):
        return self.name
