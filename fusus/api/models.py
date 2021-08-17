from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Organization(models.Model):
    """
    This class represents the Organization object in the database.
    """
    # id <-This is created by Django as the primary key, nothing to add here.
    name = models.CharField(max_length=50)  # Setting max_length to 50 to allow for long organization names.
    phone = models.CharField(max_length=20)  # Setting max_length to 20 to allow for international numbers.
    address = models.CharField(max_length=255)  # Ideally this would be broken into St Address 1, St Address 2, City,
    # State, Zip, etc.


class Profile(models.Model):
    """
    This class represents the User object in the database.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # id <-This is created by Django as the primary key, nothing to add here.
    name = models.CharField(max_length=50, blank=True)  # Setting max_length to 50 to allow for First+Middle+Last names. Ideally
    # this would be separate fields.
    phone = models.CharField(max_length=20, blank=True)  # Setting max_length to 20 to allow for international numbers.
    email = models.CharField(max_length=50, unique=True, blank=True)  # unique=True will force validation on creation to confirm
    # that this field is unique among other User models.
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)  # Might consider not using on_delete so
    # that we don't lose the user accounts when we delete the related Organization. (Many to one)
    birthdate = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()